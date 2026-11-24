import logging
from models import User, Contract, TranslatorSchedule, Job, Proposal
from services.schedule import normalize_schedule_datetime, is_schedule_complete, check_translator_schedule_conflict, ScheduleCheckError

logger = logging.getLogger(__name__)

class BookingConflictError(Exception):
    pass

class BookingValidationError(Exception):
    pass

def job_needs_time_slot(job, scheduled_date, start_time, end_time):
    """Dịch tài liệu chỉ có hạn nộp bài, không chiếm một khung giờ cố định của phiên dịch viên.

    Chỉ bỏ qua giữ chỗ khi đó là job dịch viết và không ghi ngày giờ nào. Phiên dịch
    (hoặc job dịch viết có ghi ngày giờ) vẫn bắt buộc có lịch hợp lệ.
    """
    is_document = job is not None and job.display_category_group == 'translation'
    has_any_time = any((scheduled_date, start_time, end_time))
    return not (is_document and not has_any_time)


def contract_has_no_time_slot(contract):
    """True nếu hợp đồng dịch tài liệu không có lịch giữ chỗ (nên không cần xác nhận lịch khi thanh toán)."""
    if contract.job is None or contract.job.display_category_group != 'translation':
        return False
    return TranslatorSchedule.query.filter_by(contract_id=contract.id).first() is None


def create_contract_booking(
    *,
    hirer_id,
    translator_id,
    agreed_price,
    scheduled_date,
    start_time,
    end_time,
    location=None,
    job_id=None,
    service_id=None,
    proposal_id=None,
):
    from app import db
    from sqlalchemy.exc import IntegrityError
    
    try:
        current_user = User.query.get(hirer_id)
        if not current_user:
            raise BookingValidationError("Người thuê không tồn tại.")

        translator = User.query.get(translator_id)
        if not translator or getattr(translator, 'role', '') != 'translator' or not getattr(translator, 'is_active', True):
            raise BookingValidationError("Phiên dịch viên này hiện không hoạt động hoặc không tồn tại.")

        if current_user.id == translator.id:
            raise BookingValidationError("Bạn không thể tự thuê chính mình.")

        job = None
        if job_id:
            job = (
                Job.query
                .with_for_update()
                .filter_by(id=job_id)
                .first()
            )
            if not job:
                raise BookingValidationError("Công việc không tồn tại.")
            if job.status != 'open':
                raise BookingConflictError("Công việc này không còn mở.")
                
            existing = Contract.query.filter_by(job_id=job_id).first()
            if existing:
                raise BookingConflictError("Công việc này đã được tạo hợp đồng.")

        contract = Contract(
            job_id=job_id,
            proposal_id=proposal_id,
            service_id=service_id,
            hirer_id=hirer_id,
            translator_id=translator.id,
            agreed_price=agreed_price,
            scheduled_date=scheduled_date,
            scheduled_time_start=start_time,
            scheduled_time_end=end_time,
            location=location or '',
            status='escrow_pending'
        )
        db.session.add(contract)
        db.session.flush()

        # Chốt số lượng, đơn giá và phí ngay lúc tạo hợp đồng.
        from services.payments import ensure_pricing_snapshot
        ensure_pricing_snapshot(contract)

        from services.scheduling import reserve_slot, SlotTakenError

        if job_needs_time_slot(job, scheduled_date, start_time, end_time):
            try:
                schedule = reserve_slot(
                    translator_id=translator.id,
                    scheduled_date=scheduled_date,
                    start_time=start_time,
                    end_time=end_time,
                    contract_id=contract.id,
                    job_id=job_id,
                    service_id=service_id
                )
            except SlotTakenError as e:
                raise BookingConflictError(str(e))
            except ScheduleCheckError as e:
                raise BookingValidationError(str(e))
            except Exception as e:
                raise BookingValidationError(str(e))

        if proposal_id:
            proposal = Proposal.query.get(proposal_id)
            if proposal:
                proposal.status = 'accepted'

        if job:
            job.status = 'contracted'

        from app import create_notification
        from services.notifications import should_notify
        if should_notify(translator, 'CONTRACT_CREATED'):
            try:
                create_notification(
                    user_id=translator.id,
                    notification_type='CONTRACT_CREATED',
                    title='Hợp đồng mới được tạo',
                    message=f'Khách hàng {current_user.name} đã đặt lịch với bạn.',
                    related_contract_id=contract.id
                )
            except Exception:
                pass

        db.session.commit()
        return contract

    except IntegrityError:
        db.session.rollback()
        raise BookingConflictError("Công việc này vừa được người khác đặt hoặc đã xảy ra lỗi toàn vẹn dữ liệu.")
    except (BookingConflictError, BookingValidationError, ScheduleCheckError):
        db.session.rollback()
        raise

    except Exception as e:
        db.session.rollback()
        logger.exception("Unexpected error during create_contract_booking: %s", e)
        raise BookingValidationError("đã xảy ra lỗi hệ thống khi tạo hợp đồng.") from e
