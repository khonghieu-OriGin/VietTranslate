"""Dòng tiền của hợp đồng: khách nạp, sàn giữ, giải ngân cho phiên dịch viên, rút tiền.

Mọi dòng tiền nằm trong một bảng `PaymentTransaction`, phân biệt bằng `kind`,
dùng chung cho dịch tài liệu và phiên dịch. Hàm ở đây KHÔNG tự commit;
route gọi chịu trách nhiệm commit hoặc rollback.
"""
from sqlalchemy import func

from models import db, Contract, PaymentTransaction
from services import pricing


class PaymentError(Exception):
    pass


def prior_revenue(hirer_id, translator_id, exclude_contract_id=None):
    """Doanh thu đã hoàn thành giữa đúng cặp khách và phiên dịch viên (để xét mức hoa hồng 5%)."""
    query = db.session.query(func.coalesce(func.sum(Contract.agreed_price), 0)).filter(
        Contract.hirer_id == hirer_id,
        Contract.translator_id == translator_id,
        Contract.status == 'completed',
    )
    if exclude_contract_id is not None:
        query = query.filter(Contract.id != exclude_contract_id)
    return int(query.scalar() or 0)


def ensure_pricing_snapshot(contract):
    """Chốt số lượng, đơn giá và phí vào hợp đồng. Chạy lại không đổi gì nếu đã chốt."""
    if contract.commission is not None and contract.client_fee is not None:
        return contract

    job = contract.job
    if job is not None:
        unit = pricing.normalize_unit(job.pricing_unit, job.category_group)
        quantity = pricing.normalize_quantity(job.quantity)
    else:
        # Đặt dịch vụ có sẵn (gói dịch vụ) thì tính trọn gói.
        unit, quantity = 'flat', 1

    fees = pricing.compute_fees(
        contract.agreed_price,
        prior_revenue(contract.hirer_id, contract.translator_id, exclude_contract_id=contract.id),
    )
    contract.pricing_unit = unit
    contract.quantity = quantity
    contract.unit_price = contract.agreed_price // quantity
    contract.client_fee = fees['client_fee']
    contract.commission = fees['commission']
    contract.translator_net = fees['translator_net']
    return contract


def amount_to_pay(contract):
    """Số tiền khách phải trả: giá hợp đồng cộng phí dịch vụ."""
    ensure_pricing_snapshot(contract)
    return contract.agreed_price + contract.client_fee


def record_deposit(contract, payer_id, method='sandbox'):
    """Khách thanh toán: sàn nhận và giữ tiền. Mỗi hợp đồng chỉ có một khoản nạp."""
    existing = PaymentTransaction.query.filter_by(contract_id=contract.id, kind='deposit').first()
    if existing is not None:
        return existing
    deposit = PaymentTransaction(
        contract_id=contract.id,
        user_id=payer_id,
        kind='deposit',
        amount=amount_to_pay(contract),
        status='escrow_pending',
        payment_method=method,
    )
    db.session.add(deposit)
    return deposit


def release_funds(contract):
    """Khách nghiệm thu: chuyển phần của phiên dịch viên, sàn giữ phí và hoa hồng.

    Tổng release + platform_fee luôn bằng đúng số tiền khách đã nạp.
    """
    deposit = PaymentTransaction.query.filter_by(contract_id=contract.id, kind='deposit').first()
    if deposit is None:
        # Hợp đồng cũ thanh toán trước khi có sổ giao dịch: dựng lại khoản nạp để số liệu khớp.
        deposit = record_deposit(contract, contract.hirer_id, method='legacy')
    if deposit.status != 'escrow_pending':
        raise PaymentError('Khoản tiền này không còn được giữ, không thể giải ngân.')

    ensure_pricing_snapshot(contract)
    deposit.status = 'completed'
    db.session.add(PaymentTransaction(
        contract_id=contract.id, user_id=contract.hirer_id, payee_id=contract.translator_id,
        kind='release', amount=contract.translator_net, status='completed',
        payment_method='wallet',
    ))
    db.session.add(PaymentTransaction(
        contract_id=contract.id, user_id=contract.hirer_id, payee_id=None,
        kind='platform_fee', amount=contract.client_fee + contract.commission,
        status='completed', payment_method='platform',
    ))


def wallet_balance(user_id):
    """Số dư có thể rút = tiền đã giải ngân - tiền đã rút hoặc đang chờ rút."""
    earned = db.session.query(func.coalesce(func.sum(PaymentTransaction.amount), 0)).filter(
        PaymentTransaction.kind == 'release',
        PaymentTransaction.status == 'completed',
        PaymentTransaction.payee_id == user_id,
    ).scalar()
    withdrawn = db.session.query(func.coalesce(func.sum(PaymentTransaction.amount), 0)).filter(
        PaymentTransaction.kind == 'withdraw',
        PaymentTransaction.status.in_(['pending', 'completed']),
        PaymentTransaction.payee_id == user_id,
    ).scalar()
    return int(earned or 0) - int(withdrawn or 0)


def request_withdrawal(user_id, amount):
    """Phiên dịch viên gửi yêu cầu rút tiền; admin chuyển khoản rồi đánh dấu hoàn tất."""
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        raise PaymentError('Số tiền rút không hợp lệ.')
    if amount < pricing.WITHDRAW_MIN:
        raise PaymentError(f'Số tiền rút tối thiểu là {pricing.WITHDRAW_MIN:,}đ.')
    if amount > wallet_balance(user_id):
        raise PaymentError('Số dư không đủ để rút.')

    # contract_id bắt buộc trong bảng; lấy hợp đồng gần nhất đã giải ngân cho phiên dịch viên làm mốc đối chiếu.
    anchor = PaymentTransaction.query.filter_by(
        kind='release', payee_id=user_id, status='completed'
    ).order_by(PaymentTransaction.id.desc()).first()
    withdrawal = PaymentTransaction(
        contract_id=anchor.contract_id, user_id=user_id, payee_id=user_id,
        kind='withdraw', amount=amount, status='pending', payment_method='bank_transfer',
    )
    db.session.add(withdrawal)
    return withdrawal


def complete_withdrawal(payment):
    if payment.kind != 'withdraw' or payment.status != 'pending':
        raise PaymentError('Chỉ đánh dấu hoàn tất được yêu cầu rút tiền đang chờ.')
    payment.status = 'completed'
    return payment
