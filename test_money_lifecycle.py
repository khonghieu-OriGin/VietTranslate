import os
import time
import unittest
from datetime import datetime, timedelta

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app, db
from models import User, Job, Contract, PaymentTransaction, Dispute, TranslatorViolation
from services import payments, lifecycle, refunds

NOW = datetime(2026, 12, 1, 3, 0, 0)   # UTC, tức 10:00 giờ Việt Nam


class RefundPolicyTests(unittest.TestCase):
    def test_event_table(self):
        p = refunds.event_refund_percent
        self.assertEqual(p('event', 7 * 24), 100)
        self.assertEqual(p('event', 7 * 24 - 1), 50)
        self.assertEqual(p('event', 48), 50)
        self.assertEqual(p('event', 47.9), 0)
        self.assertEqual(p('event', -3), 0)

    def test_conference_table_is_stricter(self):
        p = refunds.event_refund_percent
        self.assertEqual(p('conference', 14 * 24), 100)
        self.assertEqual(p('conference', 14 * 24 - 1), 50)
        self.assertEqual(p('conference', 7 * 24), 50)
        self.assertEqual(p('conference', 7 * 24 - 1), 0)

    def test_policy_choice(self):
        self.assertEqual(refunds.policy_for('translation', 'page', 12), 'document')
        self.assertEqual(refunds.policy_for('interpretation_other', 'hour', 3), 'event')
        self.assertEqual(refunds.policy_for('interpretation_other', 'day', 1), 'event')
        self.assertEqual(refunds.policy_for('interpretation_other', 'day', 2), 'conference')

    def test_auto_release_deadlines(self):
        t0 = datetime(2026, 12, 1, 8, 0)
        self.assertEqual(refunds.auto_release_deadline('document', 20, delivered_at=t0), t0 + timedelta(days=5))
        self.assertEqual(refunds.auto_release_deadline('document', 21, delivered_at=t0), t0 + timedelta(days=7))
        self.assertEqual(refunds.auto_release_deadline('event', 1, event_end=t0), t0 + timedelta(hours=48))
        self.assertIsNone(refunds.auto_release_deadline('document', 5))

    def test_vietnam_time_conversion(self):
        self.assertEqual(refunds.to_utc('2026-12-10', '09:00'), datetime(2026, 12, 10, 2, 0))
        self.assertIsNone(refunds.to_utc('', '09:00'))
        self.assertIsNone(refunds.to_utc('mai kia', '09:00'))


class LifecycleBase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.ctx = app.app_context()
        self.ctx.push()
        u = str(time.time()).replace('.', '')
        self.hirer = User(name='Hirer', email=f'h{u}@t.com', password_hash='x', role='hirer')
        self.trans = User(name='Trans', email=f't{u}@t.com', password_hash='x', role='translator')
        db.session.add_all([self.hirer, self.trans])
        db.session.flush()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        self.ctx.pop()

    def funded_contract(self, price=2_160_000, group='translation', unit='page', quantity=12,
                        date=None, start='09:00', end='17:00', deadline=None, paid=NOW):
        job = Job(hirer_id=self.hirer.id, title='J', description='d', status='open',
                  category_group=group, pricing_unit=unit, quantity=quantity, deadline=deadline)
        db.session.add(job)
        db.session.flush()
        c = Contract(job_id=job.id, hirer_id=self.hirer.id, translator_id=self.trans.id,
                     agreed_price=price, status='in_progress', scheduled_date=date,
                     scheduled_time_start=start if date else None, scheduled_time_end=end if date else None)
        db.session.add(c)
        db.session.flush()
        payments.record_deposit(c, self.hirer.id)
        lifecycle.mark_paid(c, now=paid)
        db.session.flush()
        return c

    def rows(self, c):
        return {r.kind: r for r in PaymentTransaction.query.filter_by(contract_id=c.id).all()}

    def assert_conserved(self, c):
        deposit = PaymentTransaction.query.filter_by(contract_id=c.id, kind='deposit').one()
        out = sum(r.amount for r in PaymentTransaction.query.filter(
            PaymentTransaction.contract_id == c.id,
            PaymentTransaction.kind.in_(['refund', 'release', 'platform_fee'])).all())
        self.assertEqual(out, deposit.amount, 'hoàn + giải ngân + phí sàn phải bằng đúng số khách đã nạp')


class DocumentCancelTests(LifecycleBase):
    def test_policy_is_snapshotted_at_payment(self):
        c = self.funded_contract()
        self.assertEqual(c.refund_policy, 'document')
        c2 = self.funded_contract(group='interpretation_other', unit='day', quantity=2, date='2026-12-20')
        self.assertEqual(c2.refund_policy, 'conference')

    def test_cancel_before_start_refunds_everything_to_wallet(self):
        c = self.funded_contract()
        kind, _ = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=2))
        db.session.flush()
        self.assertEqual(kind, 'cancelled')
        self.assertEqual(c.status, 'cancelled')
        r = self.rows(c)
        self.assertEqual(r['refund'].amount, 2_203_200)           # giá + phí 2%
        self.assertEqual((r['refund'].status, r['refund'].payment_method), ('completed', 'wallet'))
        self.assertNotIn('release', r)
        self.assertNotIn('platform_fee', r)
        self.assertEqual(payments.wallet_balance(self.hirer.id), 2_203_200)
        self.assert_conserved(c)

    def test_translator_pressing_start_ends_free_cancellation(self):
        c = self.funded_contract()
        lifecycle.start_work(c, self.trans.id, now=NOW + timedelta(hours=1))
        kind, dispute = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=2))
        self.assertEqual(kind, 'dispute')
        self.assertEqual(c.status, 'disputed')
        self.assertEqual(dispute.kind, 'cancel_working')

    def test_twelve_hours_after_payment_counts_as_started(self):
        c = self.funded_contract()
        self.assertFalse(lifecycle.has_started(c, NOW + timedelta(hours=11, minutes=59)))
        self.assertTrue(lifecycle.has_started(c, NOW + timedelta(hours=12)))
        kind, _ = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=13))
        self.assertEqual(kind, 'dispute')

    def test_only_the_hirer_can_cancel(self):
        c = self.funded_contract()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.cancel_by_hirer(c, self.trans.id, now=NOW)

    def test_cannot_cancel_twice_or_after_release(self):
        c = self.funded_contract()
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=1))
        db.session.flush()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=2))

    def test_unpaid_contract_cancels_without_money(self):
        job = Job(hirer_id=self.hirer.id, title='J', description='d', category_group='translation')
        db.session.add(job)
        db.session.flush()
        c = Contract(job_id=job.id, hirer_id=self.hirer.id, translator_id=self.trans.id,
                     agreed_price=500_000, status='escrow_pending')
        db.session.add(c)
        db.session.flush()
        kind, result = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        self.assertEqual((kind, result['refund'], c.status), ('cancelled', 0, 'cancelled'))
        self.assertEqual(PaymentTransaction.query.filter_by(contract_id=c.id).count(), 0)

    def test_late_translator_lets_hirer_cancel_with_full_refund_to_original(self):
        c = self.funded_contract(deadline=NOW.date())
        with self.assertRaises(lifecycle.LifecycleError):   # mới trễ 10 giờ
            lifecycle.cancel_for_late_delivery(c, self.hirer.id, now=datetime(2026, 12, 2, 10, 0))
        lifecycle.cancel_for_late_delivery(c, self.hirer.id, now=datetime(2026, 12, 3, 0, 1))
        db.session.flush()
        r = self.rows(c)
        self.assertEqual((r['refund'].amount, r['refund'].payment_method, r['refund'].status),
                         (2_203_200, 'original', 'pending'))
        self.assertEqual(payments.wallet_balance(self.hirer.id), 0)   # chưa về ví vì đi về phương thức gốc
        self.assert_conserved(c)

    def test_no_late_cancel_once_work_was_delivered(self):
        c = self.funded_contract(deadline=NOW.date())
        lifecycle.register_delivery(c, now=NOW + timedelta(days=1))
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.cancel_for_late_delivery(c, self.hirer.id, now=NOW + timedelta(days=5))


class EventCancelTests(LifecycleBase):
    def contract_in(self, days, **kw):
        # Sự kiện bắt đầu 09:00 giờ Việt Nam = 02:00 UTC, cách NOW đúng `days` ngày (NOW = 03:00 UTC).
        start_date = (NOW + timedelta(days=days)).date().isoformat()
        return self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=4,
                                    date=start_date, **kw)

    def test_seven_days_or_more_full_refund(self):
        c = self.contract_in(8)
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        db.session.flush()
        r = self.rows(c)
        self.assertEqual(r['refund'].amount, 1_020_000)
        self.assertNotIn('release', r)
        self.assert_conserved(c)

    def test_between_two_and_seven_days_half_refund_and_commission_only_on_kept_half(self):
        c = self.contract_in(4)
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        db.session.flush()
        r = self.rows(c)
        # Hoàn 50% giá (500.000) cộng phí 2% (20.000). Phiên dịch viên giữ 500.000, hoa hồng 10% = 50.000.
        self.assertEqual(r['refund'].amount, 520_000)
        self.assertEqual(r['release'].amount, 450_000)
        self.assertEqual(r['platform_fee'].amount, 50_000)
        self.assert_conserved(c)

    def test_under_48_hours_no_refund_and_fee_kept(self):
        c = self.contract_in(1)
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        db.session.flush()
        r = self.rows(c)
        self.assertNotIn('refund', r)
        self.assertEqual(r['release'].amount, 900_000)
        self.assertEqual(r['platform_fee'].amount, 120_000)   # 100.000 hoa hồng + 20.000 phí khách
        self.assert_conserved(c)

    def test_conference_between_seven_and_fourteen_days_is_half(self):
        start_date = (NOW + timedelta(days=10)).date().isoformat()
        c = self.funded_contract(price=5_000_000, group='interpretation_other', unit='day', quantity=2,
                                 date=start_date)
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        db.session.flush()
        self.assertEqual(self.rows(c)['refund'].amount, 2_500_000 + 100_000)
        self.assert_conserved(c)

    def test_unreadable_start_goes_to_staff_instead_of_guessing(self):
        c = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2,
                                 date='to be agreed')
        kind, dispute = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW)
        self.assertEqual(kind, 'dispute')

    def test_event_auto_release_is_48h_after_it_ends(self):
        c = self.contract_in(3)
        # kết thúc 17:00 giờ Việt Nam = 10:00 UTC
        end = datetime.combine((NOW + timedelta(days=3)).date(), datetime.min.time()) + timedelta(hours=10)
        self.assertEqual(c.auto_release_at, end + timedelta(hours=48))


class TranslatorCancelTests(LifecycleBase):
    def test_full_refund_including_fee_and_no_commission(self):
        c = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2,
                                 date=(NOW + timedelta(days=10)).date().isoformat())
        lifecycle.cancel_by_translator(c, now=NOW)
        db.session.flush()
        r = self.rows(c)
        self.assertEqual(r['refund'].amount, 1_020_000)
        self.assertNotIn('platform_fee', r)
        self.assert_conserved(c)

    def test_first_early_cancel_is_free_second_within_six_months_is_a_violation(self):
        date = (NOW + timedelta(days=10)).date().isoformat()
        a = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2, date=date)
        lifecycle.cancel_by_translator(a, now=NOW)
        db.session.flush()
        self.assertEqual(TranslatorViolation.query.filter_by(translator_id=self.trans.id).count(), 0)
        b = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2, date=date)
        lifecycle.cancel_by_translator(b, now=NOW)
        db.session.flush()
        self.assertEqual(TranslatorViolation.query.filter_by(translator_id=self.trans.id).count(), 0,
                         'vẫn chưa có vi phạm nào trước đó nên lần hai vẫn miễn')

    def test_late_cancel_is_one_violation_and_three_lock_the_account(self):
        date = (NOW + timedelta(days=2)).date().isoformat()
        for i in range(3):
            c = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2, date=date)
            lifecycle.cancel_by_translator(c, now=NOW)
            db.session.flush()
        self.assertEqual(lifecycle.violation_points(self.trans.id, 12, NOW), 3)
        self.assertFalse(self.trans.is_active)

    def test_no_show_is_two_violations_plus_ten_percent_voucher(self):
        c = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2,
                                 date=NOW.date().isoformat())
        out = lifecycle.cancel_by_translator(c, now=NOW, no_show=True)
        db.session.flush()
        self.assertEqual(out['voucher'], 100_000)
        self.assertEqual(lifecycle.violation_points(self.trans.id, 12, NOW), 2)
        r = self.rows(c)
        self.assertEqual((r['voucher'].amount, r['voucher'].payee_id), (100_000, self.hirer.id))
        self.assertEqual(payments.voucher_balance(self.hirer.id), 100_000)
        self.assertEqual(payments.wallet_balance(self.hirer.id), 1_020_000)   # voucher không nằm trong số dư rút được
        self.assert_conserved(c)

    def test_documented_illness_is_not_a_violation(self):
        c = self.funded_contract(price=1_000_000, group='interpretation_other', unit='hour', quantity=2,
                                 date=NOW.date().isoformat())
        out = lifecycle.cancel_by_translator(c, now=NOW, no_show=True, excused=True)
        db.session.flush()
        self.assertEqual(out['voucher'], 0)
        self.assertEqual(lifecycle.violation_points(self.trans.id, 12, NOW), 0)
        self.assertEqual(self.rows(c)['refund'].amount, 1_020_000)


class RevisionAndReleaseTests(LifecycleBase):
    def test_two_free_revisions_then_dispute_allowed(self):
        c = self.funded_contract()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.request_revision(c, self.hirer.id)        # chưa có bài nộp
        lifecycle.register_delivery(c, now=NOW + timedelta(days=1))
        self.assertEqual(c.auto_release_at, NOW + timedelta(days=1) + timedelta(days=5))

        with self.assertRaises(lifecycle.LifecycleError):       # chưa sửa lần nào thì chưa mở tranh chấp chất lượng
            lifecycle.open_dispute(c, self.hirer.id, 'Bản dịch sai nhiều thuật ngữ', now=NOW)

        lifecycle.request_revision(c, self.hirer.id)
        self.assertIsNone(c.auto_release_at)                    # chờ bài sửa, không tự giải ngân
        lifecycle.register_delivery(c, now=NOW + timedelta(days=2))
        self.assertEqual(c.auto_release_at, NOW + timedelta(days=2) + timedelta(days=5))   # tính lại từ đầu
        lifecycle.request_revision(c, self.hirer.id)
        lifecycle.register_delivery(c, now=NOW + timedelta(days=3))
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.request_revision(c, self.hirer.id)        # hết 2 lần

        d = lifecycle.open_dispute(c, self.hirer.id, 'Vẫn sai sau hai lần sửa bài', now=NOW + timedelta(days=4))
        self.assertEqual((c.status, d.status), ('disputed', 'open'))

    def test_long_document_gets_seven_days(self):
        c = self.funded_contract(quantity=25)
        lifecycle.register_delivery(c, now=NOW)
        self.assertEqual(c.auto_release_at, NOW + timedelta(days=7))

    def test_scheduler_releases_after_deadline_only(self):
        c = self.funded_contract()
        lifecycle.register_delivery(c, now=NOW)
        db.session.flush()
        sent = []
        stats = lifecycle.run_scheduled_jobs(now=NOW + timedelta(days=4, hours=1),
                                             notify=lambda *a: sent.append(a))
        self.assertEqual(stats['reminded'], 1)                  # còn dưới 24 giờ thì nhắc
        self.assertEqual(stats['auto_released'], 0)
        self.assertEqual(c.status, 'in_progress')

        stats = lifecycle.run_scheduled_jobs(now=NOW + timedelta(days=5, hours=1), notify=lambda *a: None)
        db.session.flush()
        self.assertEqual(stats['auto_released'], 1)
        self.assertEqual(c.status, 'completed')
        r = self.rows(c)
        self.assertEqual((r['release'].amount, r['platform_fee'].amount), (1_944_000, 259_200))
        self.assert_conserved(c)

        again = lifecycle.run_scheduled_jobs(now=NOW + timedelta(days=9), notify=lambda *a: None)
        self.assertEqual(again['auto_released'], 0)             # không giải ngân lần hai

    def test_reminder_is_sent_once(self):
        c = self.funded_contract()
        lifecycle.register_delivery(c, now=NOW)
        db.session.flush()
        t = NOW + timedelta(days=4, hours=2)
        first = lifecycle.run_scheduled_jobs(now=t, notify=lambda *a: None)
        second = lifecycle.run_scheduled_jobs(now=t + timedelta(hours=1), notify=lambda *a: None)
        self.assertEqual((first['reminded'], second['reminded']), (1, 0))

    def test_unpaid_contract_auto_cancels_after_24_hours(self):
        job = Job(hirer_id=self.hirer.id, title='J', description='d', category_group='translation')
        db.session.add(job)
        db.session.flush()
        c = Contract(job_id=job.id, hirer_id=self.hirer.id, translator_id=self.trans.id,
                     agreed_price=500_000, status='escrow_pending', created_at=NOW)
        db.session.add(c)
        db.session.flush()
        lifecycle.run_scheduled_jobs(now=NOW + timedelta(hours=23), notify=lambda *a: None)
        self.assertEqual(c.status, 'escrow_pending')
        lifecycle.run_scheduled_jobs(now=NOW + timedelta(hours=25), notify=lambda *a: None)
        self.assertEqual((c.status, c.cancelled_by), ('cancelled', 'system'))


class DisputeTests(LifecycleBase):
    def disputed(self):
        c = self.funded_contract()
        lifecycle.register_delivery(c, now=NOW)
        lifecycle.request_revision(c, self.hirer.id)
        lifecycle.register_delivery(c, now=NOW + timedelta(days=1))
        d = lifecycle.open_dispute(c, self.hirer.id, 'Bản dịch vẫn sai nhiều chỗ', now=NOW + timedelta(days=2))
        db.session.flush()
        return c, d

    def test_dispute_freezes_money_and_blocks_auto_release(self):
        c, d = self.disputed()
        self.assertIsNone(c.auto_release_at)
        stats = lifecycle.run_scheduled_jobs(now=NOW + timedelta(days=30), notify=lambda *a: None)
        self.assertEqual(stats['auto_released'], 0)
        self.assertEqual(c.status, 'disputed')
        self.assertEqual(d.evidence_deadline, NOW + timedelta(days=2, hours=48))

    def test_evidence_window_is_48_hours_and_overdue_party_is_flagged(self):
        c, d = self.disputed()
        lifecycle.submit_evidence(d, self.hirer.id, 'Ảnh chụp các lỗi', now=d.created_at or NOW + timedelta(days=2, hours=1))
        late = d.evidence_deadline + timedelta(minutes=1)
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.submit_evidence(d, self.trans.id, 'Đã nộp muộn', now=late)
        self.assertEqual(lifecycle.evidence_overdue_parties(d, now=late), ['translator'])
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.submit_evidence(d, 99999, 'người lạ', now=NOW + timedelta(days=2, hours=1))

    def test_resolve_full_refund(self):
        c, d = self.disputed()
        lifecycle.resolve_dispute(d, None, 'refund_full', note='Bản dịch không đạt', now=NOW + timedelta(days=5))
        db.session.flush()
        self.assertEqual((c.status, d.status, d.refund_percent), ('cancelled', 'resolved', 100))
        r = self.rows(c)
        self.assertEqual(r['refund'].amount, 2_203_200)
        self.assertNotIn('release', r)
        self.assert_conserved(c)

    def test_resolve_partial_keeps_work_and_charges_commission_on_translator_share_only(self):
        c, d = self.disputed()
        lifecycle.resolve_dispute(d, None, 'refund_partial', refund_percent=40, note='Lỗi một phần',
                                  now=NOW + timedelta(days=5))
        db.session.flush()
        r = self.rows(c)
        # Hoàn 40% giá = 864.000 và phí 43.200. Phiên dịch viên giữ 1.296.000, hoa hồng 10% = 129.600.
        self.assertEqual(r['refund'].amount, 864_000 + 43_200)
        self.assertEqual(r['release'].amount, 1_296_000 - 129_600)
        self.assertEqual(r['platform_fee'].amount, 129_600)
        self.assertEqual(c.status, 'completed')
        self.assert_conserved(c)

    def test_resolve_release_full(self):
        c, d = self.disputed()
        lifecycle.resolve_dispute(d, None, 'release_full', note='Bản dịch đạt', now=NOW + timedelta(days=5))
        db.session.flush()
        self.assertEqual(c.status, 'completed')
        r = self.rows(c)
        self.assertEqual((r['release'].amount, r['platform_fee'].amount), (1_944_000, 259_200))
        self.assertNotIn('refund', r)
        self.assert_conserved(c)

    def test_cannot_resolve_twice_or_with_bad_percent(self):
        c, d = self.disputed()
        for bad in (None, 0, 100, 150):
            with self.assertRaises(lifecycle.LifecycleError):
                lifecycle.resolve_dispute(d, None, 'refund_partial', refund_percent=bad)
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.resolve_dispute(d, None, 'nonsense')
        lifecycle.resolve_dispute(d, None, 'refund_full')
        db.session.flush()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.resolve_dispute(d, None, 'release_full')

    def test_cancel_while_working_defaults_to_staff_split_then_fifty_percent(self):
        c = self.funded_contract()
        lifecycle.start_work(c, self.trans.id, now=NOW + timedelta(hours=1))
        kind, d = lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=3))
        db.session.flush()
        self.assertEqual(kind, 'dispute')
        lifecycle.resolve_dispute(d, None, 'refund_partial', refund_percent=refunds.DEFAULT_WORKING_REFUND_PERCENT)
        db.session.flush()
        self.assertEqual(c.status, 'cancelled')
        self.assert_conserved(c)

    def test_short_reason_rejected(self):
        c = self.funded_contract()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.open_dispute(c, self.hirer.id, 'tệ', kind='cancel_working')


class AdminRefundAndWithdrawalTests(LifecycleBase):
    def test_settle_cannot_run_twice(self):
        c = self.funded_contract()
        lifecycle.settle(c, 100, refund_fee=True, refund_to='original', waive_commission=True, cancelled_by='admin')
        db.session.flush()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.settle(c, 100, refund_fee=True, cancelled_by='admin')

    def test_released_money_cannot_be_refunded(self):
        c = self.funded_contract()
        lifecycle.complete_contract(c)
        db.session.flush()
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle.settle(c, 100, refund_fee=True, cancelled_by='admin')

    def test_original_method_refund_waits_for_admin_and_can_be_marked_done(self):
        c = self.funded_contract()
        lifecycle.settle(c, 100, refund_fee=True, refund_to='original', cancelled_by='admin')
        db.session.flush()
        refund = self.rows(c)['refund']
        self.assertEqual(refund.status, 'pending')
        payments.complete_withdrawal(refund)
        self.assertEqual(refund.status, 'completed')
        self.assertEqual(payments.wallet_balance(self.hirer.id), 0)     # đã chuyển về nguồn gốc, không vào ví

    def test_hirer_can_withdraw_wallet_refund(self):
        c = self.funded_contract()
        lifecycle.cancel_by_hirer(c, self.hirer.id, now=NOW + timedelta(hours=1))
        db.session.flush()
        w = payments.request_withdrawal(self.hirer.id, 1_000_000)
        db.session.flush()
        self.assertEqual(w.status, 'pending')
        self.assertEqual(payments.wallet_balance(self.hirer.id), 1_203_200)

    def test_commission_helper_matches_fee_table(self):
        from services import pricing
        self.assertEqual(pricing.compute_commission(0), 0)
        self.assertEqual(pricing.compute_commission(100_000), 20_000)    # tối thiểu
        self.assertEqual(pricing.compute_commission(15_000), 15_000)     # không vượt chính số tiền
        self.assertEqual(pricing.compute_commission(2_160_000), 216_000)


if __name__ == '__main__':
    unittest.main()
