import logging
from models import User, Contract, TranslatorSchedule, Job, Proposal
from services.schedule import normalize_schedule_datetime, is_schedule_complete, check_translator_schedule_conflict, ScheduleCheckError

logger = logging.getLogger(__name__)

class BookingConflictError(Exception):
    pass

class BookingValidationError(Exception):
    pass

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
    
    try:
        current_user = User.query.get(hirer_id)
        translator = User.query.get(translator_id)

        if not translator or getattr(translator, 'role', '') != 'translator' or not getattr(translator, 'is_active', True):
            raise BookingValidationError("Phiên dịch viên này hiện không hoạt động hoặc không tồn tại.")

        if current_user.id == translator.id:
            raise BookingValidationError("Bạn không thể tự thuê chính mình.")

        if job_id:
            existing = Contract.query.filter_by(job_id=job_id).first()
            if existing:
                raise BookingConflictError("Công việc này đã được tạo hợp đồng.")

        parsed_date, parsed_start, parsed_end = normalize_schedule_datetime(
            scheduled_date, start_time, end_time
        )
        parsed = {'date': parsed_date, 'start_time': parsed_start, 'end_time': parsed_end}

        if not is_schedule_complete(parsed):
            raise BookingValidationError("Vui lòng nhập đầy đủ ngày và giờ hợp lệ.")

        conflict_result = check_translator_schedule_conflict(
            translator_id=translator.id,
            scheduled_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
        )

        if conflict_result.get('conflict'):
            raise BookingConflictError("Phiên dịch viên đã có lịch trong thời gian này.")

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

        if proposal_id:
            proposal = Proposal.query.get(proposal_id)
            if proposal:
                proposal.status = 'accepted'

        if job_id:
            job = Job.query.get(job_id)
            if job:
                job.status = 'contracted'

        db.session.flush()

        schedule = TranslatorSchedule(
            translator_id=translator.id,
            contract_id=contract.id,
            service_id=service_id,
            scheduled_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            status='reserved'
        )
        db.session.add(schedule)
        db.session.flush()

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

    except (BookingConflictError, BookingValidationError, ScheduleCheckError):
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        logger.exception("Unexpected error during create_contract_booking: %s", e)
        raise BookingValidationError("đã xảy ra lỗi hệ thống khi tạo hợp đồng.") from e
