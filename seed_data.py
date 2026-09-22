from models import db, User, TranslatorProfile, Service, Job, Proposal, Contract, Message, Deliverable, Review
from werkzeug.security import generate_password_hash
from datetime import date, datetime

def seed_data():
    """Nạp dữ liệu mẫu. Gọi trong app_context đã có sẵn bảng."""

    # === USERS ===
    admin = User(name='Admin VietTranslate', email='admin@vt.com',
                 password_hash=generate_password_hash('admin123'),
                 role='admin', is_admin=True)
    hirer1 = User(name='Nguyễn Văn A', email='hirer@test.com',
                  password_hash=generate_password_hash('123456'), role='hirer')
    hirer2 = User(name='Công ty ABC Ltd', email='hirer2@test.com',
                  password_hash=generate_password_hash('123456'), role='hirer')
    hirer3 = User(name='Trần Quốc Bảo', email='hirer3@test.com',
                  password_hash=generate_password_hash('123456'), role='hirer')

    # --- Translator: Tiếng Anh (English) ---
    trans_en = User(name='Lê Văn Cường', email='trans_en@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Nhật (Japanese) ---
    trans_jp = User(name='Trần Thị Bích', email='trans_jp@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Hàn (Korean) ---
    trans_kr = User(name='Phạm Thị Dung', email='trans_kr@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Trung (Chinese) ---
    trans_cn = User(name='Hoàng Minh Đức', email='trans_cn@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Pháp (French) ---
    trans_fr = User(name='Nguyễn Thị Mai Hương', email='trans_fr@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Đức (German) ---
    trans_de = User(name='Vũ Đình Khoa', email='trans_de@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Nga (Russian) ---
    trans_ru = User(name='Đặng Thị Thanh Hà', email='trans_ru@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Thái (Thai) ---
    trans_th = User(name='Lý Hoàng Nam', email='trans_th@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Bồ Đào Nha (Portuguese) ---
    trans_pt = User(name='Bùi Quang Huy', email='trans_pt@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')
    # --- Translator: Tiếng Tây Ban Nha (Spanish) ---
    trans_es = User(name='Ngô Thị Lan Anh', email='trans_es@test.com',
                    password_hash=generate_password_hash('123456'), role='translator')

    all_translators = [trans_en, trans_jp, trans_kr, trans_cn, trans_fr, trans_de, trans_ru, trans_th, trans_pt, trans_es]
    db.session.add_all([admin, hirer1, hirer2, hirer3] + all_translators)
    db.session.commit()

    # === TRANSLATOR PROFILES (1 per language) ===

    # Tiếng Anh - Lê Văn Cường
    prof_en = TranslatorProfile(
        user_id=trans_en.id,
        title='Biên/Phiên dịch viên tiếng Anh chuyên ngành pháp lý (IELTS 8.5)',
        bio='Thạc sĩ Luật quốc tế tại ĐH Melbourne, 5 năm dịch hợp đồng và tài liệu pháp lý cho các tổ chức quốc tế như UNDP, World Bank. Phiên dịch cabin cho hội nghị thương mại quốc tế.',
        languages='Tiếng Anh',
        badges='Rehire Badge, Local Champion',
        rating=4.7, total_reviews=32, total_jobs=40, is_verified=True
    )

    # Tiếng Nhật - Trần Thị Bích
    prof_jp = TranslatorProfile(
        user_id=trans_jp.id,
        title='Chuyên gia phiên dịch tiếng Nhật (JLPT N1)',
        bio='7 năm kinh nghiệm phiên dịch cabin và tháp tùng cho các tập đoàn Nhật Bản tại Việt Nam. Từng phiên dịch cho Toyota, Honda, Fujitsu. Tốt nghiệp ĐH Ngoại ngữ Osaka.',
        languages='Tiếng Nhật',
        badges='Rising Star, Local Champion',
        rating=4.8, total_reviews=25, total_jobs=30, is_verified=True
    )

    # Tiếng Hàn - Phạm Thị Dung
    prof_kr = TranslatorProfile(
        user_id=trans_kr.id,
        title='Phiên dịch viên tiếng Hàn (TOPIK 6) - Chuyên ngành kỹ thuật',
        bio='6 năm làm việc tại Hàn Quốc, chuyên dịch hội nghị kỹ thuật và nhà máy sản xuất Samsung, LG. Tốt nghiệp Thạc sĩ Kỹ thuật tại ĐH Seoul National.',
        languages='Tiếng Hàn',
        badges='Local Champion',
        rating=4.9, total_reviews=42, total_jobs=55, is_verified=True
    )

    # Tiếng Trung - Hoàng Minh Đức
    prof_cn = TranslatorProfile(
        user_id=trans_cn.id,
        title='Phiên dịch tiếng Trung chuyên ngành thương mại (HSK 6)',
        bio='Tốt nghiệp ĐH Bắc Kinh, HSK 6 đạt 280/300. 4 năm kinh nghiệm dịch thương mại, xuất nhập khẩu và du lịch. Thông thạo cả tiếng Trung phổ thông và Quảng Đông.',
        languages='Tiếng Trung',
        badges='Rising Star',
        rating=4.5, total_reviews=15, total_jobs=20, is_verified=True
    )

    # Tiếng Pháp - Nguyễn Thị Mai Hương
    prof_fr = TranslatorProfile(
        user_id=trans_fr.id,
        title='Biên/Phiên dịch viên tiếng Pháp (DALF C1) - Chuyên ngành ngoại giao',
        bio='Tốt nghiệp Thạc sĩ Quan hệ quốc tế tại ĐH Sorbonne, Paris. 6 năm kinh nghiệm phiên dịch cho Đại sứ quán Pháp tại Việt Nam, các tổ chức Pháp ngữ (OIF) và dự án phát triển AFD.',
        languages='Tiếng Pháp',
        badges='Rehire Badge, Rising Star',
        rating=4.7, total_reviews=20, total_jobs=28, is_verified=True
    )

    # Tiếng Đức - Vũ Đình Khoa
    prof_de = TranslatorProfile(
        user_id=trans_de.id,
        title='Phiên dịch tiếng Đức chuyên ngành kỹ thuật (Goethe C1)',
        bio='Kỹ sư cơ khí tốt nghiệp TU München (Đức), Goethe-Zertifikat C1. 5 năm phiên dịch kỹ thuật cho Bosch, Siemens, BMW tại Việt Nam. Chuyên dịch tài liệu kỹ thuật ô tô và tự động hóa.',
        languages='Tiếng Đức',
        badges='Local Champion',
        rating=4.6, total_reviews=16, total_jobs=22, is_verified=True
    )

    # Tiếng Nga - Đặng Thị Thanh Hà
    prof_ru = TranslatorProfile(
        user_id=trans_ru.id,
        title='Phiên dịch tiếng Nga chuyên ngành dầu khí & năng lượng (ТРКИ C1)',
        bio='Tốt nghiệp ĐH Tổng hợp Lomonosov (Moscow), ТРКИ cấp C1. 8 năm phiên dịch cho Vietsovpetro, Zarubezhneft và các dự án năng lượng Nga-Việt. Chuyên ngành dầu khí, khai thác mỏ.',
        languages='Tiếng Nga',
        badges='Rehire Badge, Local Champion',
        rating=4.8, total_reviews=30, total_jobs=38, is_verified=True
    )

    # Tiếng Thái - Lý Hoàng Nam
    prof_th = TranslatorProfile(
        user_id=trans_th.id,
        title='Phiên dịch tiếng Thái - Chuyên ngành du lịch & thương mại',
        bio='Sinh ra tại Thái Lan, lớn lên tại Việt Nam. Song ngữ Thái-Việt từ nhỏ. 4 năm kinh nghiệm phiên dịch du lịch, thương mại và hội chợ triển lãm. Từng dịch cho CP Group, Thai Airways.',
        languages='Tiếng Thái',
        badges='Rising Star',
        rating=4.4, total_reviews=12, total_jobs=18, is_verified=True
    )

    # Tiếng Bồ Đào Nha - Bùi Quang Huy
    prof_pt = TranslatorProfile(
        user_id=trans_pt.id,
        title='Biên dịch tiếng Bồ Đào Nha chuyên ngành xuất khẩu (CELPE-Bras Avançado)',
        bio='3 năm du học tại São Paulo, Brazil. CELPE-Bras cấp Avançado. Chuyên dịch tài liệu xuất nhập khẩu nông sản, thủy sản sang thị trường Brazil và Bồ Đào Nha. Từng dịch cho Vinamilk, Minh Phú Seafood.',
        languages='Tiếng Bồ Đào Nha',
        badges='Rising Star',
        rating=4.3, total_reviews=8, total_jobs=12, is_verified=False
    )

    # Tiếng Tây Ban Nha - Ngô Thị Lan Anh
    prof_es = TranslatorProfile(
        user_id=trans_es.id,
        title='Phiên dịch tiếng Tây Ban Nha chuyên ngành y tế & nhân đạo (DELE C1)',
        bio='Tốt nghiệp ĐH Complutense de Madrid, DELE C1. 4 năm phiên dịch cho các tổ chức nhân đạo và y tế quốc tế (MSF, Cruz Roja) tại Mỹ Latinh. Chuyên ngành y tế cộng đồng, dự án phát triển.',
        languages='Tiếng Tây Ban Nha',
        badges='Rehire Badge',
        rating=4.5, total_reviews=14, total_jobs=19, is_verified=True
    )

    all_profiles = [prof_en, prof_jp, prof_kr, prof_cn, prof_fr, prof_de, prof_ru, prof_th, prof_pt, prof_es]
    db.session.add_all(all_profiles)
    db.session.commit()

    # === SERVICES (chuyên ngành + du lịch theo ngày + du lịch theo tour) ===
    services = [
        # ── Tiếng Anh ──
        Service(profile_id=prof_en.id, name='Phiên dịch cabin hội thảo tiếng Anh',
                description='Dịch cabin đồng thời trong hội nghị quốc tế, đảm bảo tốc độ và chính xác.',
                category='Cabin', languages='Việt ↔ Anh',
                basic_price=3000000, standard_price=4500000, premium_price=7000000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_en.id, name='Biên dịch hợp đồng pháp lý tiếng Anh',
                description='Dịch hợp đồng thương mại, tài liệu pháp lý Anh-Việt. Đảm bảo thuật ngữ chuyên ngành chuẩn xác.',
                category='Dịch viết', languages='Việt ↔ Anh',
                basic_price=350000, standard_price=550000, premium_price=900000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_en.id, name='Phiên dịch du lịch theo ngày - Tiếng Anh',
                description='Đồng hành cùng khách nói tiếng Anh tham quan thành phố, di tích, chợ, bảo tàng. Hỗ trợ giao tiếp mua sắm, ẩm thực, di chuyển.',
                category='Du lịch theo ngày', languages='Việt ↔ Anh',
                basic_price=800000, standard_price=1200000, premium_price=2000000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_en.id, name='Phiên dịch du lịch theo tour - Tiếng Anh',
                description='Tháp tùng đoàn khách Anh/Mỹ/Úc xuyên suốt tour nhiều ngày: Hà Nội - Hạ Long - Huế - Hội An - HCM. Hỗ trợ check-in, đặt vé, thuyết minh di tích.',
                category='Du lịch theo tour', languages='Việt ↔ Anh',
                basic_price=3500000, standard_price=5000000, premium_price=8000000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Nhật ──
        Service(profile_id=prof_jp.id, name='Phiên dịch tháp tùng tiếng Nhật',
                description='Đi cùng đoàn khách Nhật tại sự kiện, hội nghị, thăm quan nhà máy.',
                category='Tháp tùng', languages='Việt ↔ Nhật',
                basic_price=1500000, standard_price=2500000, premium_price=4000000,
                basic_delivery='1 ngày', standard_delivery='Nửa ngày', premium_delivery='Theo yêu cầu'),
        Service(profile_id=prof_jp.id, name='Biên dịch tài liệu tiếng Nhật',
                description='Dịch hợp đồng, email, tài liệu kỹ thuật Nhật-Việt.',
                category='Dịch viết', languages='Việt ↔ Nhật',
                basic_price=300000, standard_price=500000, premium_price=900000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_jp.id, name='Phiên dịch du lịch theo ngày - Tiếng Nhật',
                description='Đồng hành cùng du khách Nhật Bản khám phá phố cổ, đền chùa, ẩm thực đường phố Việt Nam. Giới thiệu văn hóa theo phong cách omotenashi.',
                category='Du lịch theo ngày', languages='Việt ↔ Nhật',
                basic_price=1000000, standard_price=1500000, premium_price=2500000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_jp.id, name='Phiên dịch du lịch theo tour - Tiếng Nhật',
                description='Tháp tùng đoàn khách Nhật tour dài ngày: Hà Nội - Ninh Bình - Đà Nẵng - Hội An. Thuyết minh di tích, hỗ trợ onsen, ryokan style, trải nghiệm ẩm thực.',
                category='Du lịch theo tour', languages='Việt ↔ Nhật',
                basic_price=4000000, standard_price=6000000, premium_price=9000000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Hàn ──
        Service(profile_id=prof_kr.id, name='Phiên dịch hội nghị tiếng Hàn',
                description='Dịch hội nghị kỹ thuật, đào tạo nội bộ, meeting doanh nghiệp Hàn Quốc.',
                category='Hội nghị', languages='Việt ↔ Hàn',
                basic_price=2000000, standard_price=3200000, premium_price=5000000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_kr.id, name='Biên dịch tài liệu kỹ thuật tiếng Hàn',
                description='Dịch bản vẽ, hướng dẫn vận hành, tài liệu nhà máy Hàn-Việt.',
                category='Dịch viết', languages='Việt ↔ Hàn',
                basic_price=280000, standard_price=450000, premium_price=800000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_kr.id, name='Phiên dịch du lịch theo ngày - Tiếng Hàn',
                description='Đồng hành cùng du khách Hàn Quốc tham quan, mua sắm, trải nghiệm ẩm thực và làm đẹp tại Việt Nam. Hỗ trợ đặt spa, quán ăn, chợ đêm.',
                category='Du lịch theo ngày', languages='Việt ↔ Hàn',
                basic_price=900000, standard_price=1400000, premium_price=2200000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_kr.id, name='Phiên dịch du lịch theo tour - Tiếng Hàn',
                description='Tháp tùng đoàn khách Hàn tour Đà Nẵng - Hội An - Bà Nà Hills, hoặc Phú Quốc. Hỗ trợ quay vlog, check-in, trải nghiệm K-beauty & K-food Việt Nam.',
                category='Du lịch theo tour', languages='Việt ↔ Hàn',
                basic_price=3800000, standard_price=5500000, premium_price=8500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Trung ──
        Service(profile_id=prof_cn.id, name='Phiên dịch tháp tùng tiếng Trung',
                description='Tháp tùng đoàn khách Trung Quốc, hội chợ, đàm phán thương mại.',
                category='Tháp tùng', languages='Việt ↔ Trung',
                basic_price=1200000, standard_price=2000000, premium_price=3500000,
                basic_delivery='1 ngày', standard_delivery='Nửa ngày', premium_delivery='Theo yêu cầu'),
        Service(profile_id=prof_cn.id, name='Biên dịch tài liệu thương mại tiếng Trung',
                description='Dịch hợp đồng thương mại, catalogue sản phẩm, email kinh doanh Trung-Việt.',
                category='Dịch viết', languages='Việt ↔ Trung',
                basic_price=250000, standard_price=400000, premium_price=700000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_cn.id, name='Phiên dịch du lịch theo ngày - Tiếng Trung',
                description='Đồng hành cùng du khách Trung Quốc tham quan, mua sắm, thưởng thức ẩm thực. Hỗ trợ thanh toán WeChat/Alipay, đặt xe, giao tiếp chợ.',
                category='Du lịch theo ngày', languages='Việt ↔ Trung',
                basic_price=800000, standard_price=1300000, premium_price=2000000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_cn.id, name='Phiên dịch du lịch theo tour - Tiếng Trung',
                description='Tháp tùng đoàn khách Trung Quốc tour Hạ Long - Sapa - Hà Nội, hoặc Nha Trang - Đà Lạt. Thuyết minh di tích, hỗ trợ livestream bán hàng.',
                category='Du lịch theo tour', languages='Việt ↔ Trung',
                basic_price=3200000, standard_price=5000000, premium_price=7500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Pháp ──
        Service(profile_id=prof_fr.id, name='Phiên dịch hội nghị ngoại giao tiếng Pháp',
                description='Dịch cabin và nối tiếp cho hội nghị ngoại giao, sự kiện Pháp ngữ, hợp tác song phương.',
                category='Hội nghị', languages='Việt ↔ Pháp',
                basic_price=2500000, standard_price=4000000, premium_price=6500000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_fr.id, name='Biên dịch tài liệu dự án phát triển tiếng Pháp',
                description='Dịch báo cáo dự án, tài liệu ODA, hồ sơ thầu Pháp-Việt cho các tổ chức quốc tế.',
                category='Dịch viết', languages='Việt ↔ Pháp',
                basic_price=350000, standard_price=550000, premium_price=950000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_fr.id, name='Phiên dịch du lịch theo ngày - Tiếng Pháp',
                description='Đồng hành cùng du khách Pháp khám phá kiến trúc Đông Dương, phố cổ Hà Nội, Hội An. Giới thiệu di sản Pháp thuộc và ẩm thực fusion.',
                category='Du lịch theo ngày', languages='Việt ↔ Pháp',
                basic_price=900000, standard_price=1400000, premium_price=2200000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_fr.id, name='Phiên dịch du lịch theo tour - Tiếng Pháp',
                description='Tháp tùng du khách Pháp tour văn hóa: Hà Nội - Huế - Hội An - Sài Gòn. Thuyết minh lịch sử Đông Dương, thăm nhà thờ, dinh thự cổ, trải nghiệm café Việt.',
                category='Du lịch theo tour', languages='Việt ↔ Pháp',
                basic_price=4000000, standard_price=6000000, premium_price=9000000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Đức ──
        Service(profile_id=prof_de.id, name='Phiên dịch kỹ thuật tiếng Đức',
                description='Phiên dịch tại nhà máy, chuyển giao công nghệ, đào tạo kỹ thuật từ chuyên gia Đức.',
                category='Tháp tùng', languages='Việt ↔ Đức',
                basic_price=2000000, standard_price=3500000, premium_price=5500000,
                basic_delivery='1 ngày', standard_delivery='Nửa ngày', premium_delivery='Theo yêu cầu'),
        Service(profile_id=prof_de.id, name='Biên dịch tài liệu kỹ thuật ô tô tiếng Đức',
                description='Dịch hướng dẫn sử dụng, bản vẽ kỹ thuật, tiêu chuẩn DIN Đức-Việt.',
                category='Dịch viết', languages='Việt ↔ Đức',
                basic_price=350000, standard_price=550000, premium_price=950000,
                basic_delivery='4 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_de.id, name='Phiên dịch du lịch theo ngày - Tiếng Đức',
                description='Đồng hành cùng du khách Đức tham quan, đạp xe khám phá nông thôn, làng nghề truyền thống. Hỗ trợ thuê xe, giao tiếp nhà hàng, hiệu thuốc.',
                category='Du lịch theo ngày', languages='Việt ↔ Đức',
                basic_price=900000, standard_price=1400000, premium_price=2200000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_de.id, name='Phiên dịch du lịch theo tour - Tiếng Đức',
                description='Tháp tùng du khách Đức/Áo/Thụy Sĩ tour mạo hiểm: trekking Sapa, kayak Hạ Long, phượt Hà Giang. Hỗ trợ bảo hiểm, y tế, thuê trang bị.',
                category='Du lịch theo tour', languages='Việt ↔ Đức',
                basic_price=4000000, standard_price=6000000, premium_price=9500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Nga ──
        Service(profile_id=prof_ru.id, name='Phiên dịch hội nghị dầu khí tiếng Nga',
                description='Dịch cabin và nối tiếp cho hội nghị dầu khí, năng lượng, khai khoáng Nga-Việt.',
                category='Hội nghị', languages='Việt ↔ Nga',
                basic_price=2500000, standard_price=4000000, premium_price=6000000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_ru.id, name='Biên dịch tài liệu kỹ thuật dầu khí tiếng Nga',
                description='Dịch báo cáo kỹ thuật, hợp đồng khai thác, tài liệu an toàn mỏ Nga-Việt.',
                category='Dịch viết', languages='Việt ↔ Nga',
                basic_price=400000, standard_price=600000, premium_price=1000000,
                basic_delivery='4 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_ru.id, name='Phiên dịch du lịch theo ngày - Tiếng Nga',
                description='Đồng hành cùng du khách Nga tắm biển, tham quan, mua sắm tại Nha Trang, Mũi Né, Phú Quốc. Hỗ trợ đặt massage, nhà hàng hải sản, tour biển.',
                category='Du lịch theo ngày', languages='Việt ↔ Nga',
                basic_price=800000, standard_price=1300000, premium_price=2000000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_ru.id, name='Phiên dịch du lịch theo tour - Tiếng Nga',
                description='Tháp tùng đoàn khách Nga tour nghỉ dưỡng biển: Nha Trang - Đà Lạt - Phú Quốc, hoặc tour văn hóa Hà Nội - Hạ Long - Sapa. Hỗ trợ resort, spa, lặn biển.',
                category='Du lịch theo tour', languages='Việt ↔ Nga',
                basic_price=3500000, standard_price=5500000, premium_price=8500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Thái ──
        Service(profile_id=prof_th.id, name='Phiên dịch tháp tùng thương mại tiếng Thái',
                description='Tháp tùng đoàn khách Thái tại hội chợ, triển lãm, đàm phán thương mại ASEAN.',
                category='Tháp tùng', languages='Việt ↔ Thái',
                basic_price=1000000, standard_price=1800000, premium_price=3000000,
                basic_delivery='1 ngày', standard_delivery='Nửa ngày', premium_delivery='Theo yêu cầu'),
        Service(profile_id=prof_th.id, name='Biên dịch tài liệu thương mại tiếng Thái',
                description='Dịch hợp đồng, brochure, tài liệu hội chợ triển lãm Thái-Việt.',
                category='Dịch viết', languages='Việt ↔ Thái',
                basic_price=250000, standard_price=400000, premium_price=700000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_th.id, name='Phiên dịch du lịch theo ngày - Tiếng Thái',
                description='Đồng hành cùng du khách Thái Lan tham quan chùa chiền, chợ nổi, phố ẩm thực. Giới thiệu nét tương đồng văn hóa Thái-Việt, hỗ trợ đặt xe grab, mua sắm.',
                category='Du lịch theo ngày', languages='Việt ↔ Thái',
                basic_price=700000, standard_price=1100000, premium_price=1800000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_th.id, name='Phiên dịch du lịch theo tour - Tiếng Thái',
                description='Tháp tùng đoàn khách Thái Lan tour Đà Nẵng - Hội An - Bà Nà, hoặc HCM - Cần Thơ - Phú Quốc. Hỗ trợ trải nghiệm Muay Thai Việt, chùa Việt, chợ đêm.',
                category='Du lịch theo tour', languages='Việt ↔ Thái',
                basic_price=2800000, standard_price=4500000, premium_price=7000000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Bồ Đào Nha ──
        Service(profile_id=prof_pt.id, name='Biên dịch hồ sơ xuất khẩu tiếng Bồ Đào Nha',
                description='Dịch chứng nhận xuất xứ, hồ sơ xuất khẩu nông sản, thủy sản sang Brazil và Bồ Đào Nha.',
                category='Dịch viết', languages='Việt ↔ Bồ Đào Nha',
                basic_price=350000, standard_price=550000, premium_price=900000,
                basic_delivery='4 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_pt.id, name='Phiên dịch hội chợ thương mại tiếng Bồ Đào Nha',
                description='Phiên dịch tại hội chợ, triển lãm nông sản, giao thương Việt-Brazil.',
                category='Hội nghị', languages='Việt ↔ Bồ Đào Nha',
                basic_price=1800000, standard_price=3000000, premium_price=5000000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_pt.id, name='Phiên dịch du lịch theo ngày - Tiếng Bồ Đào Nha',
                description='Đồng hành cùng du khách Brazil/Bồ Đào Nha tham quan, trải nghiệm ẩm thực, khám phá phố cổ. Hỗ trợ giao tiếp chợ, nhà hàng, mua sắm.',
                category='Du lịch theo ngày', languages='Việt ↔ Bồ Đào Nha',
                basic_price=900000, standard_price=1400000, premium_price=2200000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_pt.id, name='Phiên dịch du lịch theo tour - Tiếng Bồ Đào Nha',
                description='Tháp tùng du khách Brazil tour khám phá: HCM - Mekong Delta - Phú Quốc, hoặc Hà Nội - Hạ Long - Sapa. Giới thiệu cà phê Việt, ẩm thực đường phố.',
                category='Du lịch theo tour', languages='Việt ↔ Bồ Đào Nha',
                basic_price=3500000, standard_price=5500000, premium_price=8500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),

        # ── Tiếng Tây Ban Nha ──
        Service(profile_id=prof_es.id, name='Phiên dịch hội thảo y tế tiếng Tây Ban Nha',
                description='Dịch hội thảo y tế, chương trình nhân đạo, hợp tác y tế quốc tế với đối tác Mỹ Latinh.',
                category='Hội nghị', languages='Việt ↔ Tây Ban Nha',
                basic_price=2200000, standard_price=3500000, premium_price=5500000,
                basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
        Service(profile_id=prof_es.id, name='Biên dịch tài liệu y tế & nhân đạo tiếng Tây Ban Nha',
                description='Dịch báo cáo y tế, hồ sơ bệnh án, tài liệu dự án nhân đạo Tây Ban Nha-Việt.',
                category='Dịch viết', languages='Việt ↔ Tây Ban Nha',
                basic_price=350000, standard_price=550000, premium_price=900000,
                basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
        Service(profile_id=prof_es.id, name='Phiên dịch du lịch theo ngày - Tiếng Tây Ban Nha',
                description='Đồng hành cùng du khách Tây Ban Nha/Mỹ Latinh tham quan, trải nghiệm văn hóa. Hỗ trợ giao tiếp tại chợ, quán ăn, điểm du lịch.',
                category='Du lịch theo ngày', languages='Việt ↔ Tây Ban Nha',
                basic_price=900000, standard_price=1400000, premium_price=2200000,
                basic_delivery='1 ngày (8h)', standard_delivery='1 ngày (8h)', premium_delivery='1 ngày (12h)'),
        Service(profile_id=prof_es.id, name='Phiên dịch du lịch theo tour - Tiếng Tây Ban Nha',
                description='Tháp tùng du khách nói tiếng Tây Ban Nha tour Việt Nam: Hà Nội - Huế - Hội An - HCM. Thuyết minh lịch sử, giới thiệu ẩm thực, hỗ trợ homestay.',
                category='Du lịch theo tour', languages='Việt ↔ Tây Ban Nha',
                basic_price=3500000, standard_price=5500000, premium_price=8500000,
                basic_delivery='Tour 3 ngày', standard_delivery='Tour 5 ngày', premium_delivery='Tour 7+ ngày'),
    ]
    db.session.add_all(services)
    db.session.commit()

    # === JOBS ===
    job1 = Job(hirer_id=hirer1.id,
               title='Cần phiên dịch hội thảo IT Tiếng Nhật (1 ngày)',
               description='Hội thảo giới thiệu sản phẩm phần mềm tại Q1 HCM. Yêu cầu JLPT N2 trở lên, có hiểu biết IT.',
               category='Hội thảo', source_lang='Tiếng Việt', target_lang='Tiếng Nhật',
               budget_type='range', budget_min=2000000, budget_max=4000000,
               event_date='2026-09-22', event_time_start='08:00', event_time_end='17:00',
               event_location='FPT Tower, Quận 7, TP.HCM',
               deadline=date(2026, 9, 20), status='in_progress')
    job2 = Job(hirer_id=hirer1.id,
               title='Dịch 15 trang hợp đồng mua bán Tiếng Anh',
               description='Hợp đồng mua bán thiết bị điện tử giữa công ty VN và đối tác Mỹ. Cần dịch chuyên nghiệp, có bảo mật NDA.',
               category='Dịch viết', source_lang='Tiếng Anh', target_lang='Tiếng Việt',
               budget_type='fixed', budget_min=700000,
               event_date='2026-09-25', deadline=date(2026, 9, 18), status='open')
    job3 = Job(hirer_id=hirer2.id,
               title='Phiên dịch tháp tùng đoàn khách Hàn Quốc (3 ngày)',
               description='Đoàn 8 người từ Samsung Hàn Quốc thăm quan nhà máy tại Bình Dương. Cần phiên dịch chuyên nghiệp, có kinh nghiệm kỹ thuật sản xuất.',
               category='Tháp tùng', source_lang='Tiếng Hàn', target_lang='Tiếng Việt',
               budget_type='range', budget_min=5000000, budget_max=9000000,
               event_date='2026-09-28', event_time_start='07:30', event_time_end='18:00',
               event_location='KCN VSIP, Bình Dương',
               deadline=date(2026, 9, 24), status='open')
    job4 = Job(hirer_id=hirer3.id,
               title='Phiên dịch hội nghị dầu khí Tiếng Nga (2 ngày)',
               description='Hội nghị hợp tác khai thác mỏ giữa Vietsovpetro và đối tác Nga tại Vũng Tàu. Cần phiên dịch có kinh nghiệm ngành dầu khí.',
               category='Hội nghị', source_lang='Tiếng Nga', target_lang='Tiếng Việt',
               budget_type='range', budget_min=4000000, budget_max=7000000,
               event_date='2026-10-05', event_time_start='08:30', event_time_end='17:00',
               event_location='Khách sạn Pullman, Vũng Tàu',
               deadline=date(2026, 10, 1), status='open')
    job5 = Job(hirer_id=hirer2.id,
               title='Dịch brochure sản phẩm sang Tiếng Thái (20 trang)',
               description='Cần dịch brochure giới thiệu sản phẩm nông sản Việt Nam sang tiếng Thái để trưng bày tại hội chợ Bangkok.',
               category='Dịch viết', source_lang='Tiếng Việt', target_lang='Tiếng Thái',
               budget_type='fixed', budget_min=500000,
               event_date='2026-10-10', deadline=date(2026, 10, 5), status='open')
    job6 = Job(hirer_id=hirer3.id,
               title='Biên dịch hồ sơ xuất khẩu tôm sang Tiếng Bồ Đào Nha',
               description='Dịch bộ hồ sơ xuất khẩu thủy sản (chứng nhận xuất xứ, giấy kiểm dịch) sang tiếng Bồ Đào Nha cho đối tác Brazil.',
               category='Dịch viết', source_lang='Tiếng Việt', target_lang='Tiếng Bồ Đào Nha',
               budget_type='fixed', budget_min=600000,
               event_date='2026-10-15', deadline=date(2026, 10, 10), status='open')

    db.session.add_all([job1, job2, job3, job4, job5, job6])
    db.session.commit()

    # === PROPOSALS ===
    p1 = Proposal(job_id=job1.id, translator_id=trans_jp.id,
                  cover_letter='Tôi có 7 năm dịch cabin/tháp tùng IT tiếng Nhật cho Fujitsu và FPT. Rất hân hạnh được hợp tác!',
                  price=2800000, time_estimate='1 ngày', status='accepted')
    p2 = Proposal(job_id=job2.id, translator_id=trans_en.id,
                  cover_letter='Thạc sĩ luật quốc tế, đã dịch hơn 100 bộ hợp đồng thương mại Mỹ - Việt.',
                  price=700000, time_estimate='2 ngày', status='pending')
    p3 = Proposal(job_id=job3.id, translator_id=trans_kr.id,
                  cover_letter='TOPIK 6, 6 năm làm việc tại Hàn Quốc và dịch cho các dự án Samsung Display.',
                  price=6500000, time_estimate='3 ngày', status='pending')
    p4 = Proposal(job_id=job4.id, translator_id=trans_ru.id,
                  cover_letter='8 năm phiên dịch cho Vietsovpetro, rất thông thạo thuật ngữ dầu khí Nga-Việt.',
                  price=5500000, time_estimate='2 ngày', status='pending')
    p5 = Proposal(job_id=job5.id, translator_id=trans_th.id,
                  cover_letter='Song ngữ Thái-Việt, từng dịch catalogue cho nhiều hội chợ nông sản ASEAN.',
                  price=500000, time_estimate='3 ngày', status='pending')
    p6 = Proposal(job_id=job6.id, translator_id=trans_pt.id,
                  cover_letter='Chuyên dịch hồ sơ xuất khẩu nông sản, thủy sản sang Brazil. Đã dịch cho Minh Phú Seafood.',
                  price=600000, time_estimate='4 ngày', status='pending')
    db.session.add_all([p1, p2, p3, p4, p5, p6])
    db.session.commit()

    # === CONTRACTS (Phòng làm việc trực tiếp) ===
    # Contract 1: In Progress - Hội thảo IT Nhật (Job 1)
    c1 = Contract(
        job_id=job1.id,
        proposal_id=p1.id,
        hirer_id=hirer1.id,
        translator_id=trans_jp.id,
        agreed_price=2800000,
        scheduled_date='2026-09-22',
        scheduled_time_start='08:00',
        scheduled_time_end='17:00',
        location='FPT Tower, Quận 7, TP.HCM',
        status='in_progress'
    )

    # Contract 2: Escrow Pending - Dịch vụ cabin tiếng Anh
    c2 = Contract(
        service_id=services[0].id,
        hirer_id=hirer1.id,
        translator_id=trans_en.id,
        agreed_price=3000000,
        scheduled_date='2026-09-26',
        scheduled_time_start='09:00',
        scheduled_time_end='12:00',
        location='Trung tâm Hội nghị GEM Center, Q1, TP.HCM',
        status='escrow_pending'
    )

    # Contract 3: Completed - Dịch vụ hội nghị tiếng Hàn
    c3 = Contract(
        service_id=services[8].id,
        hirer_id=hirer2.id,
        translator_id=trans_kr.id,
        agreed_price=2000000,
        scheduled_date='2026-09-10',
        scheduled_time_start='13:30',
        scheduled_time_end='17:30',
        location='Khách sạn Lotte, Hà Nội',
        status='completed'
    )

    # Contract 4: Completed - Dịch vụ ngoại giao tiếng Pháp
    c4 = Contract(
        service_id=services[16].id,
        hirer_id=hirer3.id,
        translator_id=trans_fr.id,
        agreed_price=4000000,
        scheduled_date='2026-09-05',
        scheduled_time_start='09:00',
        scheduled_time_end='16:00',
        location='Đại sứ quán Pháp, Hà Nội',
        status='completed'
    )

    # Contract 5: Completed - Dịch vụ kỹ thuật tiếng Đức
    c5 = Contract(
        service_id=services[20].id,
        hirer_id=hirer1.id,
        translator_id=trans_de.id,
        agreed_price=3500000,
        scheduled_date='2026-08-28',
        scheduled_time_start='08:00',
        scheduled_time_end='17:00',
        location='Nhà máy Bosch, Long Thành, Đồng Nai',
        status='completed'
    )

    db.session.add_all([c1, c2, c3, c4, c5])
    db.session.commit()

    # === MESSAGES & DELIVERABLES FOR CONTRACT 1 ===
    m1 = Message(contract_id=c1.id, sender_id=hirer1.id,
                 content='Chào bạn Bích, rất vui được hợp tác cùng bạn trong buổi hội thảo IT sắp tới!')
    m2 = Message(contract_id=c1.id, sender_id=trans_jp.id,
                 content='Dạ em chào anh An! Em đã nhận thông tin và đang chuẩn bị sẵn bộ thuật ngữ chuyên ngành IT cho buổi hội thảo.')
    m3 = Message(contract_id=c1.id, sender_id=hirer1.id,
                 content='Tuyệt vời, anh đã nộp tiền ký quỹ Escrow rồi nhé. Em gửi file tài liệu tham khảo khi chuẩn bị xong nhé.')
    m4 = Message(contract_id=c1.id, sender_id=trans_jp.id,
                 content='Dạ vâng anh, em gửi bản tổng hợp thuật ngữ và slide dịch nháp qua phòng làm việc đây ạ.')

    d1 = Deliverable(contract_id=c1.id, filename='Glossary_IT_Ja_Vi.docx', filepath='Glossary_IT_Ja_Vi.docx')
    db.session.add_all([m1, m2, m3, m4, d1])

    # === REVIEWS ===
    r1 = Review(contract_id=c3.id, reviewer_id=hirer2.id, reviewee_id=trans_kr.id,
                rating=5, comment='Chị Dung phiên dịch rất trôi chảy, phản xạ nhanh và tác phong vô cùng chuyên nghiệp. Nhất định sẽ tiếp tục hợp tác!')
    r2 = Review(contract_id=c4.id, reviewer_id=hirer3.id, reviewee_id=trans_fr.id,
                rating=5, comment='Chị Hương dịch ngoại giao rất chuẩn, nắm vững thuật ngữ chuyên ngành. Đối tác Pháp rất hài lòng!')
    r3 = Review(contract_id=c5.id, reviewer_id=hirer1.id, reviewee_id=trans_de.id,
                rating=4, comment='Anh Khoa dịch kỹ thuật tốt, hiểu biết sâu về lĩnh vực ô tô. Thỉnh thoảng cần thêm thời gian tra thuật ngữ chuyên sâu.')
    db.session.add_all([r1, r2, r3])
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()
    print('Seeded successfully with rich contracts & workspace data!')
