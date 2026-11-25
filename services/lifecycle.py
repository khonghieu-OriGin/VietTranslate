"""Vòng đời tiền của hợp đồng: bắt đầu, nộp bài, sửa bài, hủy, hoàn tiền, tranh chấp, tự giải ngân.

Dùng chung cho dịch tài liệu và phiên dịch; chỉ khác chính sách (`contract.refund_policy`).
Các hàm ở đây KHÔNG tự commit: route hoặc cron gọi chịu trách nhiệm commit hoặc rollback.
Mọi dòng tiền đi qua `PaymentTransaction`; mỗi lần tách tiền luôn có
hoàn + giải ngân + phí sàn = đúng số khách đã nạp.
"""
from datetime import datetime, timedelta

from models import (db, Contract, Dispute, PaymentTransaction, TranslatorProfile,
                    TranslatorSchedule, TranslatorViolation, User)
from services import payments, pricing, refunds


class LifecycleError(Exception):
    pass


# ─── Mốc thời gian ────────────────────────────────────────────────────────────

def _now(now):
    return now or datetime.utcnow()


def event_start(contract):
    return refunds.to_utc(contract.scheduled_date, contract.scheduled_time_start)


def event_end(contract):
    return refunds.to_utc(contract.scheduled_date, contract.scheduled_time_end)


def has_started(contract, now=None):
    """Đã bắt đầu làm khi bấm "Bắt đầu", hoặc 12 giờ sau khi khách thanh toán, mốc nào đến trước."""
    if contract.started_at is not None:
        return True
    if contract.paid_at is None:
        return False
    return _now(now) >= contract.paid_at + timedelta(hours=refunds.AUTO_START_HOURS)


def is_funded(contract):
    """Sàn đang giữ tiền của hợp đồng này (đã nạp, chưa giải ngân hay hoàn)."""
    return contract.status in ('in_progress', 'disputed') and PaymentTransaction.query.filter_by(
        contract_id=contract.id, kind='deposit', status='escrow_pending').first() is not None


# ─── Thanh toán, bắt đầu, nộp bài, sửa bài ────────────────────────────────────

def mark_paid(contract, now=None):
    """Khách đã thanh toán: ghi mốc giữ tiền và, với sự kiện, hạn tự giải ngân."""
    now = _now(now)
    payments.ensure_pricing_snapshot(contract)
    contract.paid_at = now
    if contract.refund_policy != 'document':
        contract.auto_release_at = refunds.auto_release_deadline(
            contract.refund_policy, contract.quantity, event_end=event_end(contract))


def start_work(contract, user_id, now=None):
    if user_id != contract.translator_id:
        raise LifecycleError('Chỉ phiên dịch viên của hợp đồng mới bấm được "Bắt đầu".')
    if contract.status != 'in_progress':
        raise LifecycleError('Phiên dịch viên chỉ bắt đầu khi hợp đồng ở trạng thái đang giữ tiền.')
    if contract.started_at is None:
        contract.started_at = _now(now)


def register_delivery(contract, now=None):
    """Phiên dịch viên nộp bài (dịch tài liệu). Hạn tự giải ngân tính lại từ đầu sau mỗi lần nộp."""
    now = _now(now)
    if contract.started_at is None:
        contract.started_at = now
    contract.delivered_at = now
    if contract.refund_policy == 'document':
        contract.auto_release_at = refunds.auto_release_deadline(
            'document', contract.quantity, delivered_at=now)
        contract.release_reminded_at = None


def request_revision(contract, user_id):
    """Khách yêu cầu sửa bài: mỗi đơn có 2 lần sửa miễn phí, chỉ cho dịch tài liệu."""
    if user_id != contract.hirer_id:
        raise LifecycleError('Chỉ khách hàng mới yêu cầu sửa bài.')
    if contract.status != 'in_progress' or contract.delivered_at is None:
        raise LifecycleError('Chỉ yêu cầu sửa được sau khi phiên dịch viên đã nộp bài.')
    if contract.refund_policy != 'document':
        raise LifecycleError('Phiên dịch tại sự kiện không áp dụng sửa bài miễn phí.')
    if (contract.revisions_used or 0) >= refunds.FREE_REVISIONS:
        raise LifecycleError('Đã hết 2 lần sửa miễn phí. Nếu bài vẫn chưa đạt, bạn có thể mở tranh chấp.')
    contract.revisions_used = (contract.revisions_used or 0) + 1
    contract.delivered_at = None
    contract.auto_release_at = None


# ─── Giải ngân ────────────────────────────────────────────────────────────────

def complete_contract(contract):
    """Nghiệm thu (khách bấm hoặc tự giải ngân): trừ hoa hồng, chuyển phần còn lại cho phiên dịch viên."""
    payments.release_funds(contract)
    contract.status = 'completed'
    contract.auto_release_at = None
    if contract.job:
        contract.job.status = 'completed'
    profile = TranslatorProfile.query.filter_by(user_id=contract.translator_id).first()
    if profile:
        profile.total_jobs = (profile.total_jobs or 0) + 1


# ─── Chia tiền khi hủy hoặc tranh chấp ────────────────────────────────────────

def settle(contract, refund_percent, *, refund_fee, refund_to='wallet', waive_commission=False,
           cancelled_by=None, reason=None, final_status='cancelled'):
    """Chia số tiền sàn đang giữ giữa khách, phiên dịch viên và sàn.

    refund_percent: phần trăm GIÁ HỢP ĐỒNG hoàn cho khách (0-100).
    refund_fee: có hoàn cả phí dịch vụ 2% hay không.
    refund_to: 'wallet' (vào ví ngay) hoặc 'original' (về phương thức gốc, admin chuyển khoản rồi đánh dấu).
    Hoa hồng chỉ tính trên phần phiên dịch viên thực nhận.
    """
    deposit = PaymentTransaction.query.filter_by(contract_id=contract.id, kind='deposit').first()
    if deposit is None or deposit.status != 'escrow_pending':
        raise LifecycleError('Khoản tiền này không còn được giữ, không thể hoàn hay chia.')
    if refund_to not in ('wallet', 'original'):
        raise LifecycleError('Nơi nhận tiền hoàn không hợp lệ.')

    payments.ensure_pricing_snapshot(contract)
    refund_percent = min(max(int(refund_percent), 0), 100)
    price = contract.agreed_price
    refund_price = price * refund_percent // 100
    translator_part = price - refund_price

    commission = 0
    if translator_part > 0 and not waive_commission:
        commission = pricing.compute_commission(
            translator_part,
            payments.prior_revenue(contract.hirer_id, contract.translator_id, exclude_contract_id=contract.id))
    translator_net = translator_part - commission
    fee_back = contract.client_fee if refund_fee else 0
    refund_total = refund_price + fee_back
    platform_fee = (contract.client_fee - fee_back) + commission

    if refund_total + translator_net + platform_fee != deposit.amount:
        raise LifecycleError('Tách tiền không khớp số đã nạp.')

    deposit.status = 'refunded' if translator_net == 0 and platform_fee == 0 else 'completed'
    if refund_total > 0:
        db.session.add(PaymentTransaction(
            contract_id=contract.id, user_id=contract.hirer_id, payee_id=contract.hirer_id,
            kind='refund', amount=refund_total,
            status='completed' if refund_to == 'wallet' else 'pending', payment_method=refund_to))
    if translator_net > 0:
        db.session.add(PaymentTransaction(
            contract_id=contract.id, user_id=contract.hirer_id, payee_id=contract.translator_id,
            kind='release', amount=translator_net, status='completed', payment_method='wallet'))
    if platform_fee > 0:
        db.session.add(PaymentTransaction(
            contract_id=contract.id, user_id=contract.hirer_id, payee_id=None,
            kind='platform_fee', amount=platform_fee, status='completed', payment_method='platform'))

    contract.status = final_status
    contract.auto_release_at = None
    if final_status == 'cancelled':
        contract.cancelled_by = cancelled_by
        contract.cancel_reason = (reason or '')[:255]
        _cancel_schedule(contract)
    if translator_net > 0 and final_status == 'completed':
        profile = TranslatorProfile.query.filter_by(user_id=contract.translator_id).first()
        if profile:
            profile.total_jobs = (profile.total_jobs or 0) + 1
    return {'refund': refund_total, 'translator_net': translator_net,
            'commission': commission, 'platform_fee': platform_fee}


def _cancel_schedule(contract):
    schedule = TranslatorSchedule.query.filter_by(contract_id=contract.id).first()
    if schedule and schedule.status in ('reserved', 'active'):
        schedule.status = 'cancelled'


def _close_job(contract, reopen):
    job = contract.job
    if job is not None and job.status in ('open', 'in_progress', 'hired', 'assigned', 'closed', 'filled'):
        job.status = 'open' if reopen else 'cancelled'


# ─── Khách hủy ────────────────────────────────────────────────────────────────

def hirer_cancel_percent(contract, now=None):
    """Phần trăm giá hợp đồng khách được hoàn khi tự hủy, hoặc None nếu cần sàn phân xử.

    Trả về (phần_trăm, lý_do).
    """
    now = _now(now)
    if contract.refund_policy == 'document':
        if not has_started(contract, now):
            return 100, 'Hủy trước khi phiên dịch viên bắt đầu làm'
        return None, 'Hủy khi phiên dịch viên đang làm, cần sàn phân xử'

    start = event_start(contract)
    if start is None:
        return None, 'Hợp đồng không có giờ bắt đầu rõ ràng, cần sàn phân xử'
    hours = refunds.hours_between(start, now)
    return refunds.event_refund_percent(contract.refund_policy, hours), 'Hủy lịch phiên dịch trước giờ bắt đầu'


def cancel_by_hirer(contract, user_id, *, now=None, refund_to='wallet', disaster=False):
    """Khách hủy hợp đồng. Trả về ('cancelled', kết_quả) hoặc ('dispute', Dispute) khi cần sàn phân xử."""
    now = _now(now)
    if user_id != contract.hirer_id:
        raise LifecycleError('Chỉ khách hàng của hợp đồng mới hủy được.')

    if contract.status == 'escrow_pending':
        contract.status = 'cancelled'
        contract.cancelled_by = 'hirer'
        contract.cancel_reason = 'Khách hủy trước khi thanh toán'
        _cancel_schedule(contract)
        _close_job(contract, reopen=True)
        return 'cancelled', {'refund': 0}
    if contract.status != 'in_progress':
        raise LifecycleError('Hợp đồng ở trạng thái này không hủy được.')

    if disaster:
        # Thiên tai, dịch bệnh, lệnh nhà nước: hoàn 100%, sàn miễn hoa hồng. Chỉ admin xác nhận được.
        raise LifecycleError('Hủy do bất khả kháng cần nhân viên sàn xác nhận, vui lòng mở tranh chấp.')

    percent, reason = hirer_cancel_percent(contract, now)
    if percent is None:
        dispute = open_dispute(contract, user_id, reason, kind='cancel_working', now=now)
        return 'dispute', dispute

    result = settle(contract, percent, refund_fee=percent > 0, refund_to=refund_to,
                    cancelled_by='hirer', reason=reason)
    _close_job(contract, reopen=False)
    return 'cancelled', result


def cancel_for_late_delivery(contract, user_id, *, now=None):
    """Phiên dịch viên trễ hạn quá 24 giờ: khách hủy ngay, hoàn 100% kể cả phí, về phương thức gốc."""
    now = _now(now)
    if user_id != contract.hirer_id:
        raise LifecycleError('Chỉ khách hàng của hợp đồng mới hủy được.')
    if contract.status != 'in_progress' or contract.delivered_at is not None:
        raise LifecycleError('Chỉ hủy vì trễ hạn được khi phiên dịch viên chưa nộp bài.')
    deadline = contract.job.deadline if contract.job is not None else None
    if deadline is None:
        raise LifecycleError('Hợp đồng không có hạn nộp bài nên không xét trễ hạn.')
    limit = datetime.combine(deadline, datetime.min.time()) + timedelta(days=1, hours=refunds.LATE_GRACE_HOURS)
    if now < limit:
        raise LifecycleError('Phiên dịch viên chưa trễ hạn quá 24 giờ.')
    result = settle(contract, 100, refund_fee=True, refund_to='original',
                    cancelled_by='hirer', reason='Phiên dịch viên trễ hạn quá 24 giờ', waive_commission=True)
    _close_job(contract, reopen=True)
    return result


# ─── Phiên dịch viên hủy hoặc vắng mặt ────────────────────────────────────────

def _lead_days(contract, now):
    start = event_start(contract)
    if start is None and contract.job is not None and contract.job.deadline is not None:
        start = datetime.combine(contract.job.deadline, datetime.min.time()) - refunds.VN_OFFSET
    if start is None:
        return 0
    return refunds.hours_between(start, now) / 24.0


def violation_points(translator_id, months, now=None):
    since = _now(now) - timedelta(days=30 * months)
    rows = TranslatorViolation.query.filter(
        TranslatorViolation.translator_id == translator_id,
        TranslatorViolation.created_at >= since).all()
    return sum(r.points or 0 for r in rows)


def _record_violation(contract, points, reason, now):
    if points <= 0:
        return
    db.session.add(TranslatorViolation(
        translator_id=contract.translator_id, contract_id=contract.id,
        points=points, reason=reason[:255], created_at=now))
    db.session.flush()
    if violation_points(contract.translator_id, refunds.VIOLATION_LOCK_MONTHS, now) >= refunds.VIOLATION_LOCK_POINTS:
        user = User.query.get(contract.translator_id)
        if user is not None:
            user.is_active = False   # khóa để sàn xem xét


def cancel_by_translator(contract, *, now=None, no_show=False, excused=False, refund_to='wallet'):
    """Phiên dịch viên hủy hoặc không đến: khách luôn được hoàn 100% kể cả phí 2%.

    - Hủy từ 7 ngày trở lên: chỉ ghi vi phạm nếu trong 6 tháng qua đã có vi phạm.
    - Hủy dưới 7 ngày: 1 vi phạm.
    - Không đến hoặc không nộp bài, không báo trước: 2 vi phạm và voucher bồi thường 10% giá hợp đồng.
    - Ốm đau, tai nạn có giấy tờ (excused): không ghi vi phạm, không voucher.
    """
    now = _now(now)
    if contract.status not in ('in_progress', 'escrow_pending'):
        raise LifecycleError('Hợp đồng ở trạng thái này không hủy được.')

    funded = contract.status == 'in_progress'
    if funded:
        settle(contract, 100, refund_fee=True, refund_to=refund_to, waive_commission=True,
               cancelled_by='translator',
               reason='Phiên dịch viên không đến' if no_show else 'Phiên dịch viên hủy')
    else:
        contract.status = 'cancelled'
        contract.cancelled_by = 'translator'
        contract.cancel_reason = 'Phiên dịch viên hủy trước khi khách thanh toán'
        _cancel_schedule(contract)
    _close_job(contract, reopen=True)

    voucher = 0
    if not excused:
        if no_show:
            _record_violation(contract, 2, 'Không đến hoặc không nộp bài, không báo trước', now)
            if funded:
                voucher = contract.agreed_price * refunds.NO_SHOW_COMPENSATION_PERCENT // 100
                if voucher > 0:
                    db.session.add(PaymentTransaction(
                        contract_id=contract.id, user_id=contract.translator_id, payee_id=contract.hirer_id,
                        kind='voucher', amount=voucher, status='completed', payment_method='voucher'))
        elif _lead_days(contract, now) >= 7:
            if violation_points(contract.translator_id, refunds.FIRST_OFFENSE_MONTHS, now) > 0:
                _record_violation(contract, 1, 'Hủy trước 7 ngày, đã có vi phạm trong 6 tháng', now)
        else:
            _record_violation(contract, 1, 'Hủy trước dưới 7 ngày', now)
    return {'voucher': voucher}


# ─── Tranh chấp ───────────────────────────────────────────────────────────────

def open_dispute(contract, user_id, reason, *, kind='quality', now=None):
    """Khách mở tranh chấp trước khi tiền được giải ngân: tiền bị đóng băng, không tự giải ngân."""
    now = _now(now)
    if user_id != contract.hirer_id:
        raise LifecycleError('Chỉ khách hàng mới mở được tranh chấp.')
    if contract.status != 'in_progress':
        raise LifecycleError('Chỉ mở được tranh chấp khi sàn còn đang giữ tiền.')
    reason = (reason or '').strip()
    if len(reason) < 10:
        raise LifecycleError('Vui lòng nêu rõ lý do tranh chấp (ít nhất 10 ký tự).')
    if kind == 'quality' and contract.refund_policy == 'document':
        if contract.delivered_at is None and (contract.revisions_used or 0) == 0:
            raise LifecycleError('Chỉ mở tranh chấp chất lượng sau khi phiên dịch viên đã nộp bài.')
        if (contract.revisions_used or 0) == 0:
            raise LifecycleError('Bạn cần yêu cầu sửa bài ít nhất một lần trước khi mở tranh chấp về chất lượng.')

    dispute = Dispute(contract_id=contract.id, opened_by=user_id, kind=kind, reason=reason,
                      hirer_evidence=reason, status='open',
                      evidence_deadline=now + timedelta(hours=refunds.EVIDENCE_HOURS))
    db.session.add(dispute)
    contract.status = 'disputed'
    contract.auto_release_at = None
    return dispute


def submit_evidence(dispute, user_id, text, now=None):
    now = _now(now)
    if dispute.status != 'open':
        raise LifecycleError('Tranh chấp đã được giải quyết.')
    if dispute.evidence_deadline and now > dispute.evidence_deadline:
        raise LifecycleError('Đã quá hạn 48 giờ nộp bằng chứng.')
    text = (text or '').strip()
    if not text:
        raise LifecycleError('Bằng chứng không được để trống.')
    contract = dispute.contract
    if user_id == contract.hirer_id:
        dispute.hirer_evidence = ((dispute.hirer_evidence or '') + '\n' + text).strip()
    elif user_id == contract.translator_id:
        dispute.translator_evidence = ((dispute.translator_evidence or '') + '\n' + text).strip()
    else:
        raise LifecycleError('Bạn không phải bên trong hợp đồng này.')


def resolve_dispute(dispute, admin_id, decision, *, refund_percent=None, note='', refund_fee=None,
                    refund_to='wallet', now=None):
    """Nhân viên tài chính quyết định: hoàn 100%, hoàn một phần, hoặc giải ngân toàn bộ."""
    now = _now(now)
    if dispute.status != 'open':
        raise LifecycleError('Tranh chấp đã được giải quyết.')
    contract = dispute.contract
    if decision == 'release_full':
        percent = 0
    elif decision == 'refund_full':
        percent = 100
    elif decision == 'refund_partial':
        if refund_percent is None or not (0 < int(refund_percent) < 100):
            raise LifecycleError('Hoàn một phần cần tỷ lệ từ 1 đến 99%.')
        percent = int(refund_percent)
    else:
        raise LifecycleError('Quyết định không hợp lệ.')

    # Tranh chấp được xử lý như hợp đồng đang giữ tiền.
    contract.status = 'in_progress'
    if decision == 'release_full':
        complete_contract(contract)
    else:
        # Tranh chấp chất lượng mà vẫn có phần trả cho phiên dịch viên thì coi như đã hoàn thành một phần.
        keeps_work = dispute.kind == 'quality' and percent < 100
        settle(contract, percent, refund_fee=(percent > 0 if refund_fee is None else refund_fee),
               refund_to=refund_to, cancelled_by='admin',
               reason=f'Tranh chấp #{dispute.id}: hoàn {percent}%',
               waive_commission=(percent == 100),
               final_status='completed' if keeps_work else 'cancelled')
        if keeps_work:
            if contract.job:
                contract.job.status = 'completed'
        else:
            _close_job(contract, reopen=False)

    dispute.status = 'resolved'
    dispute.decision = decision
    dispute.refund_percent = percent
    dispute.decision_note = (note or '').strip()
    dispute.decided_by = admin_id
    dispute.decided_at = now
    return dispute


def evidence_overdue_parties(dispute, now=None):
    """Bên chưa nộp bằng chứng khi đã hết hạn 48 giờ: sàn xem để xử thua theo điều khoản."""
    now = _now(now)
    if dispute.evidence_deadline is None or now <= dispute.evidence_deadline:
        return []
    missing = []
    if not (dispute.hirer_evidence or '').strip():
        missing.append('hirer')
    if not (dispute.translator_evidence or '').strip():
        missing.append('translator')
    return missing


# ─── Việc chạy định kỳ ────────────────────────────────────────────────────────

def run_scheduled_jobs(now=None, notify=None):
    """Chạy bởi cron mỗi ngày: hủy hợp đồng chưa thanh toán quá 24 giờ, nhắc nghiệm thu, tự giải ngân.

    notify(user_id, type, title, message, contract_id) tùy chọn, để gửi thông báo trong app.
    Trả về số lượng từng loại. Hợp đồng đang tranh chấp không bao giờ tự giải ngân.
    """
    now = _now(now)
    notify = notify or (lambda *a, **k: None)
    stats = {'unpaid_cancelled': 0, 'reminded': 0, 'auto_released': 0}

    cutoff = now - timedelta(hours=refunds.UNPAID_CANCEL_HOURS)
    for c in Contract.query.filter(Contract.status == 'escrow_pending', Contract.created_at <= cutoff).all():
        c.status = 'cancelled'
        c.cancelled_by = 'system'
        c.cancel_reason = 'Khách không thanh toán trong 24 giờ'
        _cancel_schedule(c)
        _close_job(c, reopen=True)
        notify(c.hirer_id, 'CONTRACT_CANCELLED', 'Hợp đồng đã tự hủy',
               'Hợp đồng bị hủy vì quá 24 giờ chưa thanh toán, lịch đã được nhả.', c.id)
        stats['unpaid_cancelled'] += 1

    due = Contract.query.filter(Contract.status == 'in_progress', Contract.auto_release_at.isnot(None)).all()
    for c in due:
        remaining = (c.auto_release_at - now).total_seconds() / 3600.0
        if remaining <= 0:
            try:
                complete_contract(c)
            except payments.PaymentError:
                continue
            notify(c.hirer_id, 'CONTRACT_RELEASED', 'Tiền đã tự giải ngân',
                   'Quá hạn nghiệm thu nên sàn đã giải ngân cho phiên dịch viên.', c.id)
            notify(c.translator_id, 'CONTRACT_RELEASED', 'Bạn đã nhận tiền',
                   'Khách không phản hồi đúng hạn nên tiền hợp đồng đã được giải ngân vào ví của bạn.', c.id)
            stats['auto_released'] += 1
        elif remaining <= refunds.REMINDER_HOURS and c.release_reminded_at is None:
            c.release_reminded_at = now
            notify(c.hirer_id, 'CONTRACT_REMINDER', 'Sắp hết hạn nghiệm thu',
                   'Còn dưới 24 giờ để nghiệm thu hoặc yêu cầu sửa. Quá hạn tiền sẽ tự giải ngân.', c.id)
            stats['reminded'] += 1
    return stats


# ─── Dữ liệu cho giao diện ────────────────────────────────────────────────────

POLICY_LABELS = {'document': 'Dịch tài liệu', 'event': 'Phiên dịch sự kiện', 'conference': 'Hội nghị nhiều ngày, dịch cabin'}


def panel_context(contract, now=None):
    """Những gì giao diện cần để hiện nút và mức hoàn tiền dự kiến cho từng bên."""
    now = _now(now)
    payments.ensure_pricing_snapshot(contract)
    percent, reason = (None, '')
    if contract.status == 'in_progress':
        percent, reason = hirer_cancel_percent(contract, now)
    deadline = contract.job.deadline if contract.job is not None else None
    late = False
    if contract.status == 'in_progress' and contract.delivered_at is None and deadline is not None:
        late = now >= datetime.combine(deadline, datetime.min.time()) + timedelta(days=1, hours=refunds.LATE_GRACE_HOURS)
    open_dispute_row = Dispute.query.filter_by(contract_id=contract.id, status='open').first()
    return {
        'policy_label': POLICY_LABELS.get(contract.refund_policy, ''),
        'is_document': contract.refund_policy == 'document',
        'cancel_percent': percent,
        'cancel_reason': reason,
        'cancel_refund_amount': (contract.agreed_price * percent // 100) if percent is not None else None,
        'can_start': contract.status == 'in_progress' and contract.started_at is None
                     and contract.refund_policy == 'document',
        'revisions_left': max(refunds.FREE_REVISIONS - (contract.revisions_used or 0), 0),
        'can_revise': contract.status == 'in_progress' and contract.delivered_at is not None
                      and contract.refund_policy == 'document'
                      and (contract.revisions_used or 0) < refunds.FREE_REVISIONS,
        'can_late_cancel': late,
        'dispute': open_dispute_row,
        'evidence_open': bool(open_dispute_row and open_dispute_row.evidence_deadline
                              and now <= open_dispute_row.evidence_deadline),
    }
