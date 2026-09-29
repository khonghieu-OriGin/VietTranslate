import os
import unittest
from datetime import datetime, date, time, timedelta
from app import app, db
from models import User, TranslatorSchedule, Contract, Job, TranslatorProfile
from services.scheduling import reserve_slot, confirm_slot, cancel_slot, release_expired, SlotTakenError, SchedulingError

class SchedulingTestCase(unittest.TestCase):
    def setUp(self):
        # Thiết lập context và database
        app.config['TESTING'] = True
        # Sử dụng in-memory database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Thêm dữ liệu test
        self.hirer = User(name="Hirer 1", email="hirer1@test.com", password_hash="123", role="hirer")
        self.trans1 = User(name="Trans 1", email="trans1@test.com", password_hash="123", role="translator")
        self.trans2 = User(name="Trans 2", email="trans2@test.com", password_hash="123", role="translator")
        db.session.add_all([self.hirer, self.trans1, self.trans2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_overlapping_schedules_blocked(self):
        """Lịch giao nhau cùng PDV bị chặn."""
        # Booking 1: 08:00 - 10:00
        schedule1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", buffer_before_minutes=0, buffer_after_minutes=0)
        self.assertIsNotNone(schedule1)
        
        # Booking 2: 09:00 - 11:00 -> Chặn
        with self.assertRaises(SlotTakenError):
            reserve_slot(self.trans1.id, "2024-12-01", "09:00", "11:00", buffer_before_minutes=0, buffer_after_minutes=0)

    def test_consecutive_schedules_valid(self):
        """Lịch tiếp nối hợp lệ theo quy tắc buffer."""
        # Booking 1: 08:00 - 10:00 (có 30p buffer after) => thực tế chiếm 08:00 - 10:30
        schedule1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", buffer_before_minutes=0, buffer_after_minutes=30)
        
        # Booking 2: 10:15 - 11:00 -> Chặn vì nằm trong buffer (10:00-10:30)
        with self.assertRaises(SlotTakenError):
            reserve_slot(self.trans1.id, "2024-12-01", "10:15", "11:00", buffer_before_minutes=0, buffer_after_minutes=30)
            
        # Booking 3: 10:30 - 12:00 -> Hợp lệ
        schedule3 = reserve_slot(self.trans1.id, "2024-12-01", "10:30", "12:00", buffer_before_minutes=0, buffer_after_minutes=30)
        self.assertIsNotNone(schedule3)

    def test_different_translators(self):
        """Hai PDV khác nhau cùng giờ được phép."""
        s1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", buffer_before_minutes=0, buffer_after_minutes=0)
        s2 = reserve_slot(self.trans2.id, "2024-12-01", "08:00", "10:00", buffer_before_minutes=0, buffer_after_minutes=0)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)

    def test_idempotent_request(self):
        """Request gửi lặp không tạo bản ghi trùng."""
        s1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", contract_id=999)
        s2 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", contract_id=999)
        self.assertEqual(s1.id, s2.id)

    def test_release_expired(self):
        """Reservation hết hạn được giải phóng đúng, Active không bị ảnh hưởng."""
        s1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", contract_id=101)
        s2 = reserve_slot(self.trans1.id, "2024-12-01", "14:00", "16:00", contract_id=102)
        
        # Sửa s1 lùi quá khứ 31 phút (hết hạn)
        s1.created_at = datetime.utcnow() - timedelta(minutes=31)
        # Sửa s2 thành active
        s2.status = 'active'
        db.session.commit()
        
        count = release_expired()
        self.assertEqual(count, 1)
        
        db.session.refresh(s1)
        db.session.refresh(s2)
        self.assertEqual(s1.status, 'cancelled')
        self.assertEqual(s2.status, 'active')

    def test_cancel_slot(self):
        """Hủy lịch giải phóng slot."""
        s1 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", contract_id=103)
        self.assertEqual(s1.status, 'reserved')
        cancel_slot(103)
        db.session.refresh(s1)
        self.assertEqual(s1.status, 'cancelled')
        
        # Sau khi hủy có thể đặt lịch mới
        s2 = reserve_slot(self.trans1.id, "2024-12-01", "08:00", "10:00", contract_id=104)
        self.assertIsNotNone(s2)

if __name__ == '__main__':
    unittest.main()
