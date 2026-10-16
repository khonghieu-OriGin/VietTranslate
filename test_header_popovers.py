"""
test_header_popovers.py
Unit tests for Header Settings & Help Popovers:
1. Verify popover trigger buttons (button type="button", aria-haspopup, aria-expanded, aria-controls, title).
2. Verify popovers do not navigate immediately upon click (no direct href on trigger button).
3. Verify Help Popover structure and quick actions (FAQ, Policies/Guidelines, Support tickets, CTA).
4. Verify Settings Popover structure and quick actions (Security/Password, Profile, Notifications, CTA).
5. Verify unauthenticated users do not see popovers.
6. Verify responsive bounds and accessibility attributes.
"""

import unittest
from app import app, db
from models import User


class TestHeaderPopovers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Clean old test users
        User.query.filter_by(email='test_popover_pdv@example.com').delete()
        db.session.commit()

        # Create test interpreter
        self.user = User(
            name='Nguyễn Phiên Dịch Viên',
            email='test_popover_pdv@example.com',
            password_hash='pbkdf2:sha256:dummy_popover_hash',
            role='translator'
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        try:
            User.query.filter_by(id=self.user.id).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
        self.app_context.pop()

    def _login(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id

    def test_01_authenticated_user_has_popover_structure(self):
        """Kiểm tra người dùng đã đăng nhập có đầy đủ cấu trúc Popover cho Trợ giúp & Cài đặt."""
        self._login()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')

        # Wrapper elements
        self.assertIn('id="nav-help-wrapper"', html)
        self.assertIn('id="nav-settings-wrapper"', html)

        # Trigger buttons must be <button type="button"> (not direct <a> navigation)
        self.assertIn('<button type="button" id="nav-help-btn"', html)
        self.assertIn('<button type="button" id="nav-settings-btn"', html)

        # Popover panels must be hidden by default
        self.assertIn('id="nav-help-popover"', html)
        self.assertIn('id="nav-settings-popover"', html)
        self.assertIn('class="header-popover-panel hidden', html)

        # Accessibility attributes
        self.assertIn('aria-haspopup="dialog"', html)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn('aria-controls="nav-help-popover"', html)
        self.assertIn('aria-controls="nav-settings-popover"', html)

    def test_02_help_popover_quick_items_and_cta(self):
        """Kiểm tra nội dung Popover Trợ giúp: Hỏi đáp, Hướng dẫn, Liên hệ hỗ trợ và CTA Trung tâm trợ giúp."""
        self._login()
        resp = self.client.get('/')
        html = resp.data.decode('utf-8')

        # Popover Header
        self.assertIn('Trợ giúp & Hỗ trợ', html)
        self.assertIn('Bạn cần hỗ trợ gì?', html)
        self.assertIn('24/7', html)

        # Item 1: Câu hỏi thường gặp
        self.assertIn('Câu hỏi thường gặp', html)
        self.assertIn('Tìm câu trả lời nhanh', html)
        self.assertIn('#section-support-faq', html)

        # Item 2: Hướng dẫn sử dụng
        self.assertIn('Hướng dẫn sử dụng', html)
        self.assertIn('Tìm hiểu cách sử dụng', html)
        self.assertIn('#section-support-policies', html)

        # Item 3: Liên hệ hỗ trợ
        self.assertIn('Liên hệ hỗ trợ', html)
        self.assertIn('Gửi yêu cầu hỗ trợ', html)
        self.assertIn('#section-support-tickets', html)

        # CTA Trung tâm trợ giúp
        self.assertIn('Trung tâm trợ giúp', html)

    def test_03_settings_popover_quick_items_and_cta(self):
        """Kiểm tra nội dung Popover Cài đặt: Bảo mật tài khoản, Cài đặt tài khoản, Cài đặt thông báo và CTA Xem tất cả."""
        self._login()
        resp = self.client.get('/')
        html = resp.data.decode('utf-8')

        # Popover Header
        self.assertIn('Cài đặt', html)
        self.assertIn('Quản lý tài khoản của bạn', html)

        # Item 1: Bảo mật tài khoản
        self.assertIn('Bảo mật tài khoản', html)
        self.assertIn('Mật khẩu, phiên đăng nhập', html)
        self.assertIn('#section-password-management', html)

        # Item 2: Cài đặt tài khoản
        self.assertIn('Cài đặt tài khoản', html)
        self.assertIn('Thông tin & tùy chọn', html)

        # Item 3: Cài đặt thông báo
        self.assertIn('Cài đặt thông báo', html)
        self.assertIn('Quản lý thông báo', html)
        self.assertIn('#section-notification-preferences', html)

        # CTA Xem tất cả cài đặt
        self.assertIn('Xem tất cả cài đặt', html)

    def test_04_unauthenticated_user_does_not_see_popovers(self):
        """Người dùng chưa đăng nhập không hiển thị Popover Help/Settings."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')

        self.assertNotIn('id="nav-help-popover"', html)
        self.assertNotIn('id="nav-settings-popover"', html)
        self.assertNotIn('id="nav-help-btn"', html)
        self.assertNotIn('id="nav-settings-btn"', html)

    def test_05_popover_js_and_css_animations_present(self):
        """Kiểm tra JavaScript điều khiển Popovers và CSS keyframe animation có mặt trong base template."""
        self._login()
        resp = self.client.get('/')
        html = resp.data.decode('utf-8')

        # CSS animation
        self.assertIn('@keyframes headerPopoverFadeIn', html)
        self.assertIn('.header-popover-panel:not(.hidden)', html)

        # JavaScript functions
        self.assertIn('function toggleHeaderPopover', html)
        self.assertIn('function closeAllHeaderPopovers', html)
        self.assertIn('function adjustPopoverPosition', html)
        self.assertIn('function handleHeaderPopoverNav', html)
        self.assertIn('function updateTriggerButtonState', html)


if __name__ == '__main__':
    unittest.main()
