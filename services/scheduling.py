import logging
from datetime import datetime, timedelta, date, time
from sqlalchemy.exc import IntegrityError
from models import User, TranslatorSchedule
from app import db
from services.schedule import (
    normalize_schedule_datetime,
    is_schedule_complete,
    check_translator_schedule_conflict,
    build_effective_interval,
    ScheduleCheckError
)

logger = logging.getLogger(__name__)

class SchedulingError(Exception):
    pass

class SlotTakenError(SchedulingError):
    pass

def _resolve_datetime_to_utc(local_date: date, local_time: time) -> datetime:
    """Helper để chuẩn hóa timezone UTC khi lưu nếu cần (hiện tại schema đang dùng Date/Time)."""
    # Vì schema gốc lưu db.Date và db.Time mà không có timezone (naive), ta sẽ tuân thủ nguyên tắc "không sửa data type/schema cũ".
    # PostgreSQL sẽ lưu theo timezone mặc định của DB (hoặc naive). 
    # Nếu phải có timezone, ta sẽ cần đổi schema. Ở đây tạm thời giữ nguyên kiểu cũ.
    dt = datetime.combine(local_date, local_time)
    return dt

def busy_ranges(translator_id, check_date: date):
    """
    Trả về danh sách các khoảng thời gian bị chiếm dụng (sau khi cộng/trừ buffer) 
    của một phiên dịch viên trong một ngày cụ thể.
    """
    schedules = (
        TranslatorSchedule.query
        .filter_by(translator_id=translator_id, scheduled_date=check_date)
        .filter(TranslatorSchedule.status.in_(['reserved', 'active']))
        .all()
    )
    ranges = []
    for s in schedules:
        start_dt, end_dt = build_effective_interval(
            s.scheduled_date, s.start_time, s.end_time, s.buffer_before_minutes, s.buffer_after_minutes
        )
        ranges.append({'start': start_dt, 'end': end_dt, 'contract_id': s.contract_id})
    return ranges

def release_expired():
    """
    Giải phóng các lịch đang ở trạng thái 'reserved' nhưng đã hết hạn (quá 30 phút mà chưa thanh toán/xác nhận).
    """
    threshold = datetime.utcnow() - timedelta(minutes=30)
    expired_schedules = (
        TranslatorSchedule.query
        .filter_by(status='reserved')
        .filter(TranslatorSchedule.created_at < threshold)
        .all()
    )
    
    count = 0
    for s in expired_schedules:
        s.status = 'cancelled'
        count += 1
        
    if count > 0:
        db.session.commit()
        logger.info(f"Released {count} expired schedule reservations.")
    return count

def reserve_slot(
    translator_id, 
    scheduled_date, 
    start_time, 
    end_time, 
    contract_id=None,
    job_id=None,
    service_id=None,
    buffer_before_minutes=0,
    buffer_after_minutes=30
):
    """
    Giữ chỗ (reserve) một slot cho phiên dịch viên.
    Sẽ raise SlotTakenError nếu trùng lịch.
    """
    # 1. Giải phóng reservation cũ trước khi kiểm tra (tránh false positive)
    release_expired()
    
    # 2. Chuẩn hóa & kiểm tra tính hợp lệ
    parsed_date, parsed_start, parsed_end = normalize_schedule_datetime(
        scheduled_date, start_time, end_time
    )
    parsed = {'date': parsed_date, 'start_time': parsed_start, 'end_time': parsed_end}
    if not is_schedule_complete(parsed):
        raise SchedulingError("Thời gian đặt lịch không hợp lệ hoặc bị thiếu.")

    try:
        # 3. Sử dụng row-level locking để ngăn chặn race condition trên cấp ứng dụng.
        # Lấy bản ghi user để lock
        translator = User.query.with_for_update().filter_by(id=translator_id).first()
        if not translator or getattr(translator, 'role', '') != 'translator':
            raise SchedulingError("Phiên dịch viên không tồn tại.")
        
        # Kiểm tra tính Idempotent: nếu đã có reservation với contract_id này thì trả về luôn
        if contract_id:
            existing = TranslatorSchedule.query.filter_by(contract_id=contract_id).first()
            if existing:
                return existing

        # 4. Kiểm tra overlap (có tính buffer)
        conflict_result = check_translator_schedule_conflict(
            translator_id=translator_id,
            scheduled_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            buffer_before_minutes=buffer_before_minutes,
            buffer_after_minutes=buffer_after_minutes
        )
        if conflict_result.get('conflict'):
            raise SlotTakenError(conflict_result.get('message', "Lịch bị trùng với một booking khác."))

        # 5. Tạo bản ghi reservation trong cùng transaction
        schedule = TranslatorSchedule(
            translator_id=translator_id,
            contract_id=contract_id,
            job_id=job_id,
            service_id=service_id,
            scheduled_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            buffer_before_minutes=buffer_before_minutes,
            buffer_after_minutes=buffer_after_minutes,
            status='reserved'
        )
        db.session.add(schedule)
        db.session.flush() # Gửi xuống DB để kiểm tra exclusion constraint (nếu có Postgres)
        
        return schedule
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"PostgreSQL exclusion constraint or unique constraint triggered: {e}")
        raise SlotTakenError("Lịch đã bị chiếm bởi một giao dịch đồng thời.")
    except Exception as e:
        if not isinstance(e, SchedulingError):
            logger.exception("Unexpected error in reserve_slot")
        raise

def confirm_slot(contract_id):
    """
    Chuyển trạng thái từ reserved sang active khi đã thanh toán thành công (escrow).
    """
    schedule = TranslatorSchedule.query.filter_by(contract_id=contract_id, status='reserved').first()
    if not schedule:
        return False
        
    schedule.status = 'active'
    db.session.commit()
    return True

def cancel_slot(contract_id):
    """
    Giải phóng slot (chuyển sang cancelled) khi hủy hợp đồng hoặc đổi lịch.
    """
    schedule = TranslatorSchedule.query.filter_by(contract_id=contract_id).first()
    if schedule and schedule.status in ['reserved', 'active']:
        schedule.status = 'cancelled'
        db.session.commit()
        return True
    return False
