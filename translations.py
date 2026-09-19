# -*- coding: utf-8 -*-
"""
VietTranslate Internationalization (i18n) Module
Contains localized string dictionaries for Vietnamese (vi) and English (en),
along with helper functions for string lookup and dynamic language list localization.
"""

TRANSLATIONS = {
    'vi': {
        # ─── Navigation & Base Layout ───
        'nav': {
            'brand_subtitle': 'Mạng Lưới Ngôn Ngữ Toàn Cầu',
            'find_translators': 'Tìm Phiên Dịch',
            'jobs': 'Việc Làm',
            'about': 'Giới Thiệu',
            'payment_escrow': 'Thanh Toán & Escrow',
            'post_job': 'Đăng Job',
            'admin': 'Quản Trị',
            'login': 'Đăng Nhập',
            'register': 'Đăng Ký',
            'account_profile': 'Hồ Sơ Tài Khoản',
            'contract_history': 'Lịch Sử Hợp Đồng',
            'logout': 'Đăng Xuất',
            'mobile_post_job': '+ Đăng Job Mới',
            'admin_dashboard': '⚙️ Bảng Quản Trị',
            'switch_language': 'Ngôn ngữ giao diện',
            'lang_vi': 'Tiếng Việt',
            'lang_en': 'English',
        },

        # ─── Footer ───
        'footer': {
            'tagline': 'Nền tảng kết nối ngôn ngữ hiện đại. Uy tín trong từng kết nối, chất lượng trong từng trải nghiệm giữa khách hàng và phiên dịch viên chuyên nghiệp.',
            'escrow_guarantee': 'Bảo vệ Escrow 100%',
            'core_languages_badge': '10+ Ngôn ngữ chính',
            'col_services_title': 'Dịch Vụ & Việc Làm',
            'col_services_find': 'Tìm Phiên Dịch Viên',
            'col_services_jobs': 'Cơ Hội Việc Làm',
            'col_services_post': 'Đăng Tin Tuyển Dụng',
            'col_services_escrow': 'Cơ Chế Escrow An Toàn',
            'col_languages_title': 'Khám Phá Theo Ngôn Ngữ',
            'col_support_title': 'Hỗ Trợ & Thông Tin',
            'col_support_about': 'Về VietTranslate',
            'col_support_refund': 'Chính Sách Hoàn Tiền',
            'col_support_join': 'Gia nhập đội ngũ phiên dịch',
            'copyright': '© 2026 VietTranslate. Nền tảng kết nối ngôn ngữ chất lượng cao.',
            'terms': 'Điều khoản sử dụng',
            'privacy': 'Chính sách bảo mật',
        },

        # ─── Home / Hero Section ───
        'hero': {
            'badge': 'Nền tảng kết nối phiên dịch viên toàn cầu',
            'headline_line1': 'Kết Nối Ngôn Ngữ.',
            'headline_line2': 'Mở Lối Cơ Hội.',
            'subtitle': 'Uy tín trong từng kết nối. Chất lượng trong từng trải nghiệm.',
            'intent_label': 'Tôi cần',
            'intent_translator': 'Tìm phiên dịch viên',
            'intent_job': 'Tìm việc phiên dịch',
            'lang_label': 'Ngôn ngữ',
            'all_languages': 'Tất cả ngôn ngữ',
            'service_label': 'Loại dịch vụ',
            'all_services': 'Tất cả loại hình',
            'service_conference': 'Phiên dịch hội nghị & sự kiện',
            'service_business': 'Đàm phán thương mại & B2B',
            'service_court': 'Phiên dịch pháp lý & thủ tục',
            'service_tech': 'Kỹ thuật, công nghệ & nhà máy',
            'service_document': 'Dịch thuật tài liệu chuyên sâu',
            'keyword_label': 'Từ khóa tìm kiếm',
            'keyword_placeholder': 'VD: Cabin, đàm phán FDI, y tế...',
            'search_button': 'Tìm Kiếm Ngay',
            'popular_tags_label': 'Tìm kiếm nhanh:',
        },

        # ─── Home / Stats Bar ───
        'stats': {
            'translators_count': '5,200+',
            'translators_label': 'Phiên dịch viên chuyên nghiệp',
            'satisfaction_rate': '99.4%',
            'satisfaction_label': 'Tỷ lệ khách hàng hài lòng',
            'contracts_count': '12,400+',
            'contracts_label': 'Hợp đồng hoàn thành thành công',
            'escrow_amount': '100%',
            'escrow_label': 'Quỹ thanh toán bảo vệ Escrow',
        },

        # ─── Home / Language Strip ───
        'home_languages': {
            'badge': 'Ngôn ngữ phổ biến',
            'title': 'Hỗ Trợ Toàn Diện 10+ Ngôn Ngữ Trọng Tâm',
            'subtitle': 'Mỗi ngôn ngữ đều có đội ngũ phiên dịch viên đã qua kiểm tra chứng chỉ quốc tế và kinh nghiệm thực chiến.',
            'view_all': 'Xem tất cả phiên dịch viên',
            'translators_suffix': 'chuyên gia',
        },

        # ─── Home / Featured Translators ───
        'featured_translators': {
            'badge': 'Đội ngũ xuất sắc',
            'title': 'Phiên Dịch Viên Tiêu Biểu',
            'subtitle': 'Những chuyên gia ngôn ngữ có số giờ phiên dịch cao, đánh giá 5 sao và uy tín hàng đầu trên hệ thống.',
            'view_all_btn': 'Xem Tất Cả Hồ Sơ',
            'reviews_suffix': 'đánh giá',
            'jobs_completed_suffix': 'dự án hoàn thành',
            'price_from': 'Từ',
            'per_day': 'ngày',
            'per_hour': 'giờ',
            'view_profile_btn': 'Xem Hồ Sơ',
            'book_now_btn': 'Đặt Lịch Ngay',
        },

        # ─── Home / Latest Jobs ───
        'latest_jobs': {
            'badge': 'Cơ hội mới',
            'title': 'Việc Làm Mới Nhất',
            'subtitle': 'Khám phá các dự án phiên dịch và dịch thuật đang chờ báo giá từ các doanh nghiệp và cá nhân.',
            'view_all_btn': 'Xem Tất Cả Việc Làm',
            'budget_label': 'Ngân sách dự kiến',
            'proposals_suffix': 'đề xuất',
            'deadline_label': 'Hạn chốt:',
            'apply_btn': 'Gửi Báo Giá',
            'negotiable': 'Thỏa thuận',
            'empty_message': 'Hiện chưa có công việc mới nào.',
        },

        # ─── Home / 8-Step International Standard Workflow ───
        'workflow': {
            'badge': 'Quy trình chuẩn mực',
            'title': 'Quy Trình Làm Việc 8 Bước Chuẩn Quốc Tế',
            'subtitle': 'Hệ thống vận hành khép kín đảm bảo quyền lợi tối đa cho cả người thuê và phiên dịch viên.',
            'step1_num': '01',
            'step1_title': 'Đăng Yêu Cầu',
            'step1_desc': 'Mô tả nhu cầu, ngôn ngữ, địa điểm, thời gian và mức ngân sách dự kiến.',
            'step2_num': '02',
            'step2_title': 'Nhận Báo Giá',
            'step2_desc': 'Các phiên dịch viên phù hợp gửi đề xuất phương án và mức thù lao cạnh tranh.',
            'step3_num': '03',
            'step3_title': 'Chọn Ứng Viên',
            'step3_desc': 'Xem hồ sơ, kiểm tra chứng chỉ, phỏng vấn trực tiếp trước khi quyết định.',
            'step4_num': '04',
            'step4_title': 'Ký Quỹ Escrow',
            'step4_desc': 'Người thuê thanh toán vào quỹ bảo chứng an toàn của VietTranslate.',
            'step5_num': '05',
            'step5_title': 'Thực Hiện Hợp Đồng',
            'step5_desc': 'Phiên dịch viên tiến hành công việc theo đúng cam kết về chất lượng và thời gian.',
            'step6_num': '06',
            'step6_title': 'Bàn Giao & Nghiệm Thu',
            'step6_desc': 'Khách hàng đánh giá kết quả công việc hoặc tài liệu đã hoàn thành.',
            'step7_num': '07',
            'step7_title': 'Giải Ngân Quỹ',
            'step7_desc': 'Hệ thống chuyển tiền thù lao cho phiên dịch viên ngay khi được phê duyệt.',
            'step8_num': '08',
            'step8_title': 'Đánh Giá Song Phương',
            'step8_desc': 'Hai bên chấm điểm và nhận xét công khai để xây dựng uy tín cộng đồng.',
        },

        # ─── Home / Why Us & Trust ───
        'trust': {
            'badge': 'Cam kết vững chắc',
            'title': 'Tại Sao Hơn 10,000+ Khách Hàng Tin Chọn VietTranslate?',
            'subtitle': 'Chúng tôi đặt chất lượng bản dịch và sự an tâm tài chính của bạn lên hàng đầu.',
            'feature1_title': 'Bảo Vệ Escrow Toàn Diện',
            'feature1_desc': 'Tiền chỉ được giải ngân khi bạn hoàn toàn hài lòng với chất lượng phiên dịch.',
            'feature2_title': 'Thẩm Định Chứng Chỉ Kỹ Lưỡng',
            'feature2_desc': '100% hồ sơ hiển thị đều qua xác minh danh tính và bằng cấp chuyên môn (IELTS, JLPT, HSK, TOPIK...).',
            'feature3_title': 'Hỗ Trợ Xử Lý Tranh Chấp 24/7',
            'feature3_desc': 'Đội ngũ chuyên viên can thiệp và bảo vệ quyền lợi của cả hai bên trong vòng 24h làm việc.',
            'feature4_title': 'Bảo Mật Thông Tin Nghiêm Ngặt',
            'feature4_desc': 'Ký cam kết bảo mật (NDA) tự động cho mọi tài liệu kinh doanh và sự kiện kín.',
        },

        # ─── Home / CTA Banner ───
        'cta': {
            'title': 'Sẵn Sàng Nâng Tầm Giao Tiếp Toàn Cầu?',
            'subtitle': 'Đăng ký ngay hôm nay để kết nối với các chuyên gia ngôn ngữ hàng đầu hoặc tìm kiếm dự án phiên dịch mơ ước.',
            'btn_hire': 'Thuê Phiên Dịch Viên Ngay',
            'btn_join': 'Gia Nhập Đội Ngũ Chuyên Gia',
        },

        # ─── About Page ───
        'about_page': {
            'title': 'Về VietTranslate | Nền Tảng Ngôn Ngữ Toàn Cầu',
            'badge': 'Sứ mệnh của chúng tôi',
            'headline': 'Kết Nối Ngôn Ngữ <br><span class="text-brand-600">Mở Lối Cơ Hội.</span>',
            'intro': 'VietTranslate là nền tảng marketplace kết nối trực tiếp giữa các doanh nghiệp, tổ chức và chuyên gia phiên dịch hàng đầu trên toàn cầu.',
            'pillar1_title': 'Mạng Lưới Quốc Tế',
            'pillar1_desc': 'Hơn 5,000+ chuyên gia phiên dịch Cabin, tháp tùng, đàm phán thương mại đã qua thẩm định hồ sơ và chứng chỉ (JLPT N1, IELTS 8.0+, TOPIK 6...).',
            'pillar2_title': 'Bảo Vệ Quỹ Escrow',
            'pillar2_desc': '100% hợp đồng được ký quỹ tạm giữ an toàn. Giải ngân chuẩn xác sau khi khách hàng hài lòng và nghiệm thu kết quả.',
            'pillar3_title': 'Nhanh Chóng & Trực Tiếp',
            'pillar3_desc': 'Trao đổi 1-on-1 trực tiếp, không qua trung gian đôn giá, xem lịch khả dụng thời gian thực và chốt hợp đồng chỉ trong vài phút.',
            'stat_languages': 'Ngôn ngữ toàn cầu',
            'stat_experts': 'Chuyên gia ngôn ngữ',
            'stat_projects': 'Dự án hoàn thành',
            'stat_satisfaction': 'Đánh giá hài lòng',
        },

        # ─── Payment & Escrow Page ───
        'payment_page': {
            'title': 'Cơ Chế Escrow & Bảo Vệ Thanh Toán | VietTranslate',
            'badge': 'An toàn tuyệt đối',
            'headline': 'Thanh Toán & Bảo Vệ Giao Dịch (Escrow)',
            'intro': 'VietTranslate đóng vai trò là bên thứ ba trung gian uy tín, bảo đảm quyền lợi tài chính và chất lượng dịch vụ cho cả hai bên.',
            'process_title': 'Quy Trình Vận Hành Quỹ Bảo Chứng',
            'process_subtitle': '3 bước minh bạch bảo vệ 100% rủi ro bùng tiền hoặc không giao việc.',
            'step1_title': 'Tạm Giữ Tiền (Escrow)',
            'step1_desc': 'Khách hàng thanh toán vào tài khoản quỹ trung gian của VietTranslate khi hai bên thống nhất hợp đồng.',
            'step2_title': 'Yên Tâm Thực Hiện',
            'step2_desc': 'Hệ thống xác nhận tiền đã sẵn sàng trong quỹ. Phiên dịch viên an tâm hoàn toàn để cống hiến chất lượng tốt nhất.',
            'step3_title': 'Nghiệm Thu & Giải Ngân',
            'step3_desc': 'Sau khi sự kiện/bản dịch hoàn tất đạt yêu cầu, khách hàng bấm phê duyệt và tiền tự động chuyển về tài khoản chuyên gia.',
            'policy_title': 'Chính Sách Cam Kết & Hoàn Tiền',
            'policy_item1_label': 'Hoàn tiền 100%:',
            'policy_item1_text': 'Áp dụng nếu phiên dịch viên vắng mặt, hủy ca đột xuất hoặc không bàn giao tài liệu như đã ký kết.',
            'policy_item2_label': 'Hỗ trợ giải quyết tranh chấp:',
            'policy_item2_text': 'Ban quản trị VietTranslate tham gia đối soát chứng từ, ghi âm, bản dịch trong vòng 24 giờ làm việc.',
            'policy_item3_label': '99.4% tỉ lệ hài lòng:',
            'policy_item3_text': 'Hơn 12,000+ hợp đồng giao dịch an toàn không phát sinh tranh chấp.',
        },

        # ─── Authentication (Login & Register) ───
        'auth': {
            'login_title': 'Đăng Nhập | VietTranslate',
            'login_badge': 'Tài Khoản VietTranslate',
            'login_headline': 'Đăng Nhập',
            'login_sub': 'Truy cập nền tảng kết nối phiên dịch hàng đầu',
            'google_login': 'Đăng nhập với Google',
            'or_email': 'Hoặc email',
            'email_label': 'Email',
            'password_label': 'Mật khẩu',
            'forgot_password': 'Quên mật khẩu?',
            'login_button': 'Đăng Nhập',
            'no_account': 'Chưa có tài khoản?',
            'register_link': 'Đăng ký thành viên',
            'register_title': 'Đăng Ký Tài Khoản | VietTranslate',
            'register_badge': 'Tham gia mạng lưới',
            'register_headline': 'Tạo Tài Khoản Mới',
            'register_sub': 'Gia nhập nền tảng ngôn ngữ chuyên nghiệp hàng đầu',
            'role_label': 'Chọn vai trò của bạn',
            'role_hirer': 'Người Thuê',
            'role_hirer_desc': 'Tìm và thuê phiên dịch',
            'role_translator': 'Phiên Dịch Viên',
            'role_translator_desc': 'Nhận dự án & làm việc',
            'fullname_label': 'Họ và tên',
            'fullname_placeholder': 'VD: Hoàng Minh Nhật',
            'phone_label': 'Số điện thoại',
            'phone_placeholder': '0901234567',
            'work_email_label': 'Email công việc',
            'work_email_placeholder': 'name@company.com',
            'password_placeholder': 'Tối thiểu 6 ký tự',
            'register_button': 'Đăng Ký Ngay',
            'have_account': 'Đã có tài khoản?',
            'login_link': 'Đăng nhập',
        },

        # ─── Translator List Page ───
        'translator_list_page': {
            'title': 'Tìm Phiên Dịch Viên Chuyên Nghiệp | VietTranslate',
            'header_title': 'Tìm Kiếm Phiên Dịch Viên Chuyên Nghiệp',
            'header_subtitle': 'Khám phá và kết nối với các chuyên gia ngôn ngữ hàng đầu, được đánh giá minh bạch bởi khách hàng thực tế.',
            'filter_language_title': 'Ngôn Ngữ Phiên Dịch',
            'filter_specialty_title': 'Chuyên Ngành Phiên Dịch',
            'filter_service_title': 'Hình Thức Dịch Vụ',
            'filter_price_title': 'Mức Giá (VNĐ/giờ)',
            'filter_rating_title': 'Đánh Giá Tối Thiểu',
            'filter_btn_reset': 'Đặt Lại Bộ Lọc',
            'filter_btn_apply': 'Áp Dụng Lọc',
            'sort_by_label': 'Sắp xếp theo:',
            'sort_rating_high': 'Đánh giá cao nhất',
            'sort_reviews_many': 'Nhiều đánh giá nhất',
            'sort_price_low': 'Giá thấp đến cao',
            'sort_price_high': 'Giá cao đến thấp',
            'sort_jobs_many': 'Nhiều dự án nhất',
            'showing_count': 'Hiển thị',
            'translators_count_label': 'chuyên gia',
            'no_results_title': 'Không tìm thấy phiên dịch viên phù hợp',
            'no_results_desc': 'Hãy thử điều chỉnh bộ lọc hoặc xóa bớt tiêu chí tìm kiếm để xem thêm kết quả.',
            'contact_btn': 'Nhắn Tin',
            'book_btn': 'Đặt Lịch',
            'view_profile_btn': 'Xem Chi Tiết',
        },

        # ─── Job List Page ───
        'job_list_page': {
            'title': 'Bảng Tin Việc Làm Dịch Thuật | VietTranslate',
            'badge': 'Thị trường việc làm dịch thuật',
            'header_title': 'Bảng Tin Việc Làm Dịch Thuật',
            'header_subtitle': 'Tiếp cận các dự án dịch thuật trực tiếp từ doanh nghiệp và cá nhân. Minh bạch ngân sách, an tâm Escrow.',
            'post_job_cta': '+ Đăng tin tuyển dụng mới',
            'filter_title': 'Bộ lọc việc làm',
            'filter_lang': 'Ngôn ngữ',
            'filter_type': 'Loại Hình Công Việc',
            'filter_budget': 'Mức ngân sách',
            'filter_time': 'Thời gian đăng',
            'time_today': 'Hôm nay',
            'time_3days': '3 ngày gần nhất',
            'time_7days': '7 ngày gần nhất',
            'time_30days': '30 ngày gần nhất',
            'time_all': 'Tất cả',
            'budget_all': 'Tất cả mức giá',
            'budget_under_1m': 'Dưới 1,000,000 đ',
            'budget_1m_5m': '1,000,000 đ - 5,000,000 đ',
            'budget_5m_15m': '5,000,000 đ - 15,000,000 đ',
            'budget_over_15m': 'Trên 15,000,000 đ',
            'search_placeholder': 'Tìm kiếm theo tiêu đề, kỹ năng...',
            'showing_count': 'Hiển thị',
            'open_jobs_label': 'việc làm đang mở',
            'sort_label': 'Sắp xếp:',
            'sort_newest': 'Mới nhất',
            'sort_budget_desc': 'Ngân sách cao nhất',
            'sort_budget_asc': 'Ngân sách thấp nhất',
            'sort_proposals_asc': 'Ít đề xuất nhất',
            'fixed_price': 'Giá cố định',
            'budget_range_label': 'Khoảng ngân sách',
            'negotiable': 'Thương lượng',
            'posted_on': 'Đăng ngày',
            'proposals_count': 'đề xuất',
            'no_proposals_yet': 'Chưa có đề xuất',
            'deadline': 'Hạn nộp:',
            'posted_by': 'Đăng bởi:',
            'apply_proposal': 'Gửi Đề Xuất',
            'view_details': 'Xem Chi Tiết',
            'reset_filter': 'Xóa lọc',
            'reset_all_filters': 'Xóa tất cả bộ lọc',
            'apply_filter': 'Áp dụng',
            'no_jobs_available': 'Hiện chưa có việc làm nào đang mở.',
            'no_match_title': 'Không tìm thấy việc làm phù hợp',
            'no_match_desc': 'Hãy thử thay đổi hoặc xóa bớt tiêu chí lọc để khám phá thêm nhiều cơ hội mới.',
        },

        # ─── Common / Alerts ───
        'common': {
            'all': 'Tất cả',
            'verified': 'Đã xác minh',
            'status_open': 'Đang tuyển',
            'status_assigned': 'Đã giao việc',
            'status_in_progress': 'Đang thực hiện',
            'status_completed': 'Đã hoàn thành',
            'status_cancelled': 'Đã hủy',
            'currency': 'đ',
            'save': 'Lưu lại',
            'cancel': 'Hủy bỏ',
            'confirm': 'Xác nhận',
            'back': 'Quay lại',
            'loading': 'Đang tải...',
        }
    },

    'en': {
        # ─── Navigation & Base Layout ───
        'nav': {
            'brand_subtitle': 'Global Language Hub',
            'find_translators': 'Find Translators',
            'jobs': 'Jobs',
            'about': 'About Us',
            'payment_escrow': 'Payment & Escrow',
            'post_job': 'Post a Job',
            'admin': 'Admin',
            'login': 'Log In',
            'register': 'Sign Up',
            'account_profile': 'Account Profile',
            'contract_history': 'Contract History',
            'logout': 'Log Out',
            'mobile_post_job': '+ Post a New Job',
            'admin_dashboard': '⚙️ Admin Dashboard',
            'switch_language': 'Interface Language',
            'lang_vi': 'Tiếng Việt',
            'lang_en': 'English',
        },

        # ─── Footer ───
        'footer': {
            'tagline': 'Modern language connection platform. Trust in every connection, excellence in every experience between clients and professional language experts.',
            'escrow_guarantee': '100% Escrow Protection',
            'core_languages_badge': '10+ Core Languages',
            'col_services_title': 'Services & Jobs',
            'col_services_find': 'Find Translators',
            'col_services_jobs': 'Career Opportunities',
            'col_services_post': 'Post a Project',
            'col_services_escrow': 'Secure Escrow System',
            'col_languages_title': 'Explore by Language',
            'col_support_title': 'Support & Info',
            'col_support_about': 'About VietTranslate',
            'col_support_refund': 'Refund Policy',
            'col_support_join': 'Join as a Translator',
            'copyright': '© 2026 VietTranslate. Premium Language Connection Platform.',
            'terms': 'Terms of Service',
            'privacy': 'Privacy Policy',
        },

        # ─── Home / Hero Section ───
        'hero': {
            'badge': 'Global Professional Language Platform',
            'headline_line1': 'Connecting Languages.',
            'headline_line2': 'Unlocking Opportunities.',
            'subtitle': 'Trust in every connection. Excellence in every experience.',
            'intent_label': 'I need to',
            'intent_translator': 'Find a translator / interpreter',
            'intent_job': 'Find translation jobs',
            'lang_label': 'Language',
            'all_languages': 'All Languages',
            'service_label': 'Service Type',
            'all_services': 'All Service Types',
            'service_conference': 'Conference & Simultaneous',
            'service_business': 'Business Negotiation & B2B',
            'service_court': 'Legal & Courtroom',
            'service_tech': 'Technical, Factory & Engineering',
            'service_document': 'Specialized Document Translation',
            'keyword_label': 'Search keyword',
            'keyword_placeholder': 'e.g., Cabin, FDI negotiation, medical...',
            'search_button': 'Search Now',
            'popular_tags_label': 'Popular searches:',
        },

        # ─── Home / Stats Bar ───
        'stats': {
            'translators_count': '5,200+',
            'translators_label': 'Certified Professional Translators',
            'satisfaction_rate': '99.4%',
            'satisfaction_label': 'Client Satisfaction Rate',
            'contracts_count': '12,400+',
            'contracts_label': 'Successfully Completed Contracts',
            'escrow_amount': '100%',
            'escrow_label': 'Escrow-Protected Payment Fund',
        },

        # ─── Home / Language Strip ───
        'home_languages': {
            'badge': 'Popular Languages',
            'title': 'Comprehensive Support for 10+ Key Languages',
            'subtitle': 'Each language is backed by a verified roster of linguists with recognized international certificates and industry expertise.',
            'view_all': 'View all translators',
            'translators_suffix': 'experts',
        },

        # ─── Home / Featured Translators ───
        'featured_translators': {
            'badge': 'Top Rated',
            'title': 'Featured Interpreters & Translators',
            'subtitle': 'Distinguished language professionals with extensive hours, 5-star ratings, and proven platform track records.',
            'view_all_btn': 'View All Profiles',
            'reviews_suffix': 'reviews',
            'jobs_completed_suffix': 'projects completed',
            'price_from': 'From',
            'per_day': 'day',
            'per_hour': 'hour',
            'view_profile_btn': 'View Profile',
            'book_now_btn': 'Book Service',
        },

        # ─── Home / Latest Jobs ───
        'latest_jobs': {
            'badge': 'New Opportunities',
            'title': 'Latest Projects & Job Postings',
            'subtitle': 'Discover active translation and interpreting requests open for proposals from businesses and clients.',
            'view_all_btn': 'Browse All Jobs',
            'budget_label': 'Estimated Budget',
            'proposals_suffix': 'proposals',
            'deadline_label': 'Deadline:',
            'apply_btn': 'Submit Proposal',
            'negotiable': 'Negotiable',
            'empty_message': 'No open job listings at the moment.',
        },

        # ─── Home / 8-Step International Standard Workflow ───
        'workflow': {
            'badge': 'Standard Workflow',
            'title': '8-Step International Standard Workflow',
            'subtitle': 'A transparent, closed-loop process guaranteeing security and fairness for both clients and translators.',
            'step1_num': '01',
            'step1_title': 'Post Project Requirements',
            'step1_desc': 'Detail your language pair, scope, location, schedule, and allocated budget.',
            'step2_num': '02',
            'step2_title': 'Receive Competitive Proposals',
            'step2_desc': 'Qualified translators review your job and send customized bids with clear timelines.',
            'step3_num': '03',
            'step3_title': 'Select the Best Candidate',
            'step3_desc': 'Compare credentials, certifications, past client reviews, and conduct interviews.',
            'step4_num': '04',
            'step4_title': 'Fund Escrow Deposit',
            'step4_desc': 'The client deposits funds securely into the VietTranslate third-party escrow vault.',
            'step5_num': '05',
            'step5_title': 'Execute the Contract',
            'step5_desc': 'The translator delivers the assignment adhering strictly to the agreed standards.',
            'step6_num': '06',
            'step6_title': 'Review Deliverables',
            'step6_desc': 'The client inspects the completed translation or confirms event attendance satisfaction.',
            'step7_num': '07',
            'step7_title': 'Release Escrow Payout',
            'step7_desc': 'Payment is instantly released to the translator once client approval is confirmed.',
            'step8_num': '08',
            'step8_title': 'Mutual Ratings & Feedback',
            'step8_desc': 'Both parties leave verified feedback to build trust and community reputation.',
        },

        # ─── Home / Why Us & Trust ───
        'trust': {
            'badge': 'Guaranteed Excellence',
            'title': 'Why 10,000+ Clients Trust VietTranslate',
            'subtitle': 'We place uncompromising translation fidelity and ironclad financial safety at the core of our platform.',
            'feature1_title': 'Complete Escrow Protection',
            'feature1_desc': 'Funds are only disbursed after you are 100% satisfied with the delivered work.',
            'feature2_title': 'Rigorous Credential Verification',
            'feature2_desc': 'All listed profiles undergo identity audits and diploma verification (IELTS, JLPT, HSK, TOPIK, etc.).',
            'feature3_title': '24/7 Dispute Resolution',
            'feature3_desc': 'Our dedicated mediation team reviews project logs, audio recordings, and text files within 24 hours.',
            'feature4_title': 'Strict Confidentiality (NDA)',
            'feature4_desc': 'Automated non-disclosure agreements protect your corporate data, proprietary files, and private events.',
        },

        # ─── Home / CTA Banner ───
        'cta': {
            'title': 'Ready to Elevate Your Global Communication?',
            'subtitle': 'Join today to connect with top-tier language specialists or discover your next rewarding translation project.',
            'btn_hire': 'Hire a Translator Now',
            'btn_join': 'Join as a Specialist',
        },

        # ─── About Page ───
        'about_page': {
            'title': 'About VietTranslate | Global Language Platform',
            'badge': 'Our Mission',
            'headline': 'Connecting Languages <br><span class="text-brand-600">Unlocking Opportunities.</span>',
            'intro': 'VietTranslate is a premier marketplace bridging businesses, institutions, and elite linguists worldwide.',
            'pillar1_title': 'International Network',
            'pillar1_desc': 'Over 5,000+ simultaneous, consecutive, and business negotiation specialists verified with top certifications (JLPT N1, IELTS 8.0+, TOPIK 6...).',
            'pillar2_title': 'Escrow Safeguards',
            'pillar2_desc': '100% of contracts are secured in an escrow holding account. Payouts are executed smoothly upon verified completion.',
            'pillar3_title': 'Fast & Direct Collaboration',
            'pillar3_desc': 'Direct 1-on-1 communication without agency markups, real-time availability checks, and contract finalization in minutes.',
            'stat_languages': 'Global Languages',
            'stat_experts': 'Language Experts',
            'stat_projects': 'Completed Projects',
            'stat_satisfaction': 'Satisfaction Score',
        },

        # ─── Payment & Escrow Page ───
        'payment_page': {
            'title': 'Escrow Mechanism & Payment Protection | VietTranslate',
            'badge': 'Absolute Safety',
            'headline': 'Payment & Transaction Protection (Escrow)',
            'intro': 'VietTranslate operates as a trusted neutral third party, safeguarding financial integrity and service quality for both parties.',
            'process_title': 'How the Escrow Vault Operates',
            'process_subtitle': 'A transparent 3-step mechanism that eliminates 100% of non-payment and non-delivery risks.',
            'step1_title': 'Deposit Funds (Escrow)',
            'step1_desc': 'The client deposits the agreed compensation into VietTranslate safe escrow fund upon signing the contract.',
            'step2_title': 'Worry-Free Execution',
            'step2_desc': 'The system confirms funds are secured. The linguist can work with total focus on providing the highest quality.',
            'step3_title': 'Inspection & Disbursement',
            'step3_desc': 'After the event or translated document meets quality standards, the client approves release and funds transfer instantly.',
            'policy_title': 'Guarantees & Refund Policy',
            'policy_item1_label': '100% Money-Back Guarantee:',
            'policy_item1_text': 'Applies if a translator fails to attend an assignment, cancels unexpectedly, or does not deliver agreed files.',
            'policy_item2_label': 'Dispute Resolution Support:',
            'policy_item2_text': 'VietTranslate administrators review recordings, time stamps, and deliverables within 24 business hours.',
            'policy_item3_label': '99.4% Satisfaction Rate:',
            'policy_item3_text': 'Over 12,000+ successfully completed transactions without unresolved disputes.',
        },

        # ─── Authentication (Login & Register) ───
        'auth': {
            'login_title': 'Log In | VietTranslate',
            'login_badge': 'VietTranslate Account',
            'login_headline': 'Sign In',
            'login_sub': 'Access the premier language services marketplace',
            'google_login': 'Sign in with Google',
            'or_email': 'Or use email',
            'email_label': 'Email Address',
            'password_label': 'Password',
            'forgot_password': 'Forgot password?',
            'login_button': 'Sign In',
            'no_account': "Don't have an account?",
            'register_link': 'Sign up now',
            'register_title': 'Create an Account | VietTranslate',
            'register_badge': 'Join Our Network',
            'register_headline': 'Create New Account',
            'register_sub': 'Join the leading network of language professionals and clients',
            'role_label': 'Select your role',
            'role_hirer': 'Client / Hirer',
            'role_hirer_desc': 'Find & hire translators',
            'role_translator': 'Translator / Linguist',
            'role_translator_desc': 'Find projects & work',
            'fullname_label': 'Full Name',
            'fullname_placeholder': 'e.g., Alex Johnson',
            'phone_label': 'Phone Number',
            'phone_placeholder': '+84 901 234 567',
            'work_email_label': 'Business Email',
            'work_email_placeholder': 'name@company.com',
            'password_placeholder': 'Minimum 6 characters',
            'register_button': 'Create Account',
            'have_account': 'Already have an account?',
            'login_link': 'Sign in',
        },

        # ─── Translator List Page ───
        'translator_list_page': {
            'title': 'Find Professional Translators & Interpreters | VietTranslate',
            'header_title': 'Find Certified Language Specialists',
            'header_subtitle': 'Discover and connect with top-tier translators and interpreters, verified and reviewed by real clients.',
            'filter_language_title': 'Languages',
            'filter_specialty_title': 'Specialties',
            'filter_service_title': 'Service Formats',
            'filter_price_title': 'Hourly Rate (VND/hour)',
            'filter_rating_title': 'Minimum Rating',
            'filter_btn_reset': 'Reset Filters',
            'filter_btn_apply': 'Apply Filters',
            'sort_by_label': 'Sort by:',
            'sort_rating_high': 'Highest Rated',
            'sort_reviews_many': 'Most Reviewed',
            'sort_price_low': 'Price: Low to High',
            'sort_price_high': 'Price: High to Low',
            'sort_jobs_many': 'Most Projects Done',
            'showing_count': 'Showing',
            'translators_count_label': 'specialists',
            'no_results_title': 'No matching translators found',
            'no_results_desc': 'Try adjusting your filters or search terms to explore more qualified linguists.',
            'contact_btn': 'Message',
            'book_btn': 'Book Service',
            'view_profile_btn': 'View Profile',
        },

        # ─── Job List Page ───
        'job_list_page': {
            'title': 'Translation & Interpreting Job Board | VietTranslate',
            'badge': 'Translation Job Marketplace',
            'header_title': 'Translation & Interpreting Job Board',
            'header_subtitle': 'Access direct translation projects from businesses and individuals. Transparent budgets, secure Escrow.',
            'post_job_cta': '+ Post a New Job',
            'filter_title': 'Job Filters',
            'filter_lang': 'Languages',
            'filter_type': 'Job Category',
            'filter_budget': 'Budget Range',
            'filter_time': 'Posted Within',
            'time_today': 'Today',
            'time_3days': 'Past 3 days',
            'time_7days': 'Past 7 days',
            'time_30days': 'Past 30 days',
            'time_all': 'All time',
            'budget_all': 'All budgets',
            'budget_under_1m': 'Under 1,000,000 VND',
            'budget_1m_5m': '1,000,000 - 5,000,000 VND',
            'budget_5m_15m': '5,000,000 - 15,000,000 VND',
            'budget_over_15m': 'Above 15,000,000 VND',
            'search_placeholder': 'Search by title, skills, keywords...',
            'showing_count': 'Showing',
            'open_jobs_label': 'open jobs',
            'sort_label': 'Sort by:',
            'sort_newest': 'Newest',
            'sort_budget_desc': 'Highest budget',
            'sort_budget_asc': 'Lowest budget',
            'sort_proposals_asc': 'Fewest proposals',
            'fixed_price': 'Fixed Price',
            'budget_range_label': 'Budget Range',
            'negotiable': 'Negotiable',
            'posted_on': 'Posted on',
            'proposals_count': 'proposals',
            'no_proposals_yet': 'No proposals yet',
            'deadline': 'Deadline:',
            'posted_by': 'Posted by:',
            'apply_proposal': 'Submit Proposal',
            'view_details': 'View Details',
            'reset_filter': 'Clear',
            'reset_all_filters': 'Clear all filters',
            'apply_filter': 'Apply',
            'no_jobs_available': 'No active jobs available right now.',
            'no_match_title': 'No matching jobs found',
            'no_match_desc': 'Try adjusting or clearing your filters to explore more opportunities.',
        },

        # ─── Common / Alerts ───
        'common': {
            'all': 'All',
            'verified': 'Verified',
            'status_open': 'Open',
            'status_assigned': 'Assigned',
            'status_in_progress': 'In Progress',
            'status_completed': 'Completed',
            'status_cancelled': 'Cancelled',
            'currency': 'VND',
            'save': 'Save',
            'cancel': 'Cancel',
            'confirm': 'Confirm',
            'back': 'Back',
            'loading': 'Loading...',
        }
    }
}


# Language metadata mapping for dynamic display
LOCALIZED_LANGUAGES_DATA = [
    {
        'code': 'GB',
        'code_lower': 'gb',
        'flag': '🇬🇧',
        'slug': 'english',
        'name_vi': 'Tiếng Anh',
        'name_en': 'English',
        'short_name_vi': 'Anh',
        'short_name_en': 'English',
        'cert_vi': 'IELTS / TOEIC / VSTEP',
        'cert_en': 'IELTS / TOEIC / VSTEP',
    },
    {
        'code': 'JP',
        'code_lower': 'jp',
        'flag': '🇯🇵',
        'slug': 'japanese',
        'name_vi': 'Tiếng Nhật',
        'name_en': 'Japanese',
        'short_name_vi': 'Nhật',
        'short_name_en': 'Japanese',
        'cert_vi': 'JLPT N2 trở lên',
        'cert_en': 'JLPT N2 or higher',
    },
    {
        'code': 'KR',
        'code_lower': 'kr',
        'flag': '🇰🇷',
        'slug': 'korean',
        'name_vi': 'Tiếng Hàn',
        'name_en': 'Korean',
        'short_name_vi': 'Hàn',
        'short_name_en': 'Korean',
        'cert_vi': 'TOPIK 4 trở lên',
        'cert_en': 'TOPIK Level 4+',
    },
    {
        'code': 'CN',
        'code_lower': 'cn',
        'flag': '🇨🇳',
        'slug': 'chinese',
        'name_vi': 'Tiếng Trung',
        'name_en': 'Chinese',
        'short_name_vi': 'Trung',
        'short_name_en': 'Chinese',
        'cert_vi': 'HSK 5 trở lên',
        'cert_en': 'HSK Level 5+',
    },
    {
        'code': 'FR',
        'code_lower': 'fr',
        'flag': '🇫🇷',
        'slug': 'french',
        'name_vi': 'Tiếng Pháp',
        'name_en': 'French',
        'short_name_vi': 'Pháp',
        'short_name_en': 'French',
        'cert_vi': 'DELF B2 trở lên',
        'cert_en': 'DELF B2 or higher',
    },
    {
        'code': 'DE',
        'code_lower': 'de',
        'flag': '🇩🇪',
        'slug': 'german',
        'name_vi': 'Tiếng Đức',
        'name_en': 'German',
        'short_name_vi': 'Đức',
        'short_name_en': 'German',
        'cert_vi': 'TestDaF / Goethe B2',
        'cert_en': 'TestDaF / Goethe B2',
    },
    {
        'code': 'RU',
        'code_lower': 'ru',
        'flag': '🇷🇺',
        'slug': 'russian',
        'name_vi': 'Tiếng Nga',
        'name_en': 'Russian',
        'short_name_vi': 'Nga',
        'short_name_en': 'Russian',
        'cert_vi': 'ТРКИ B2 trở lên',
        'cert_en': 'TORFL B2 or higher',
    },
    {
        'code': 'TH',
        'code_lower': 'th',
        'flag': '🇹🇭',
        'slug': 'thai',
        'name_vi': 'Tiếng Thái',
        'name_en': 'Thai',
        'short_name_vi': 'Thái',
        'short_name_en': 'Thai',
        'cert_vi': 'Kiểm tra trực tiếp',
        'cert_en': 'Direct Assessment',
    },
    {
        'code': 'PT',
        'code_lower': 'pt',
        'flag': '🇵🇹',
        'slug': 'portuguese',
        'name_vi': 'Tiếng Bồ Đào Nha',
        'name_en': 'Portuguese',
        'short_name_vi': 'Bồ Đào Nha',
        'short_name_en': 'Portuguese',
        'cert_vi': 'CELPE-Bras',
        'cert_en': 'CELPE-Bras',
    },
    {
        'code': 'ES',
        'code_lower': 'es',
        'flag': '🇪🇸',
        'slug': 'spanish',
        'name_vi': 'Tiếng Tây Ban Nha',
        'name_en': 'Spanish',
        'short_name_vi': 'Tây Ban Nha',
        'short_name_en': 'Spanish',
        'cert_vi': 'DELE B2 trở lên',
        'cert_en': 'DELE B2 or higher',
    },
]


def t(key, lang='vi', **kwargs):
    """
    Look up a localized string key in dot notation (e.g. 'nav.find_translators').
    Falls back to 'vi' if not found in 'en', or returns the key if not found in either.
    Formats with kwargs if specified.
    """
    if not lang or lang not in ('vi', 'en'):
        lang = 'vi'

    parts = key.split('.')
    cur = TRANSLATIONS.get(lang, {})
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            cur = None
            break

    # Fallback to Vietnamese if English missing
    if cur is None and lang != 'vi':
        cur = TRANSLATIONS.get('vi', {})
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                cur = None
                break

    if cur is None:
        return key

    if kwargs and isinstance(cur, str):
        try:
            return cur.format(**kwargs)
        except Exception:
            return cur

    return cur


def get_localized_languages(lang='vi'):
    """
    Returns the list of languages formatted for templates, with names localized
    to the active language.
    """
    is_en = (lang == 'en')
    result = []
    for item in LOCALIZED_LANGUAGES_DATA:
        display_name = item['name_en'] if is_en else item['name_vi']
        short_name = item['short_name_en'] if is_en else item['short_name_vi']
        cert = item['cert_en'] if is_en else item['cert_vi']
        flag_alt = f"{short_name} flag" if is_en else f"Quốc kỳ {short_name}"
        
        entry = {
            'name': display_name,
            'name_vi': item['name_vi'],
            'name_en': item['name_en'],
            'flag': item['flag'],
            'cert': cert,
            'code': item['code'],
            'short_name': short_name,
            'code_lower': item['code_lower'],
            'flag_svg': f"https://flagcdn.com/{item['code_lower']}.svg",
            'flag_alt': flag_alt,
            'slug': item['slug']
        }
        result.append(entry)
    return result
