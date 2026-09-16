from app import app, db
from models import User, TranslatorProfile, Service, Job, Proposal, Contract, Message, Deliverable, Review
from werkzeug.security import generate_password_hash
from datetime import date, datetime

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # === USERS ===
        admin = User(name='Admin VietTranslate', email='admin@vt.com',
                     password_hash=generate_password_hash('admin123'),
                     role='admin', is_admin=True)
        hirer1 = User(name='Nguyễn Văn A', email='hirer@test.com',
                      password_hash=generate_password_hash('123456'), role='hirer')
        hirer2 = User(name='Công ty ABC Ltd', email='hirer2@test.com',
                      password_hash=generate_password_hash('123456'), role='hirer')
        trans1 = User(name='Trần Thị Bích', email='trans1@test.com',
                      password_hash=generate_password_hash('123456'), role='translator')
        trans2 = User(name='Lê Văn Cường', email='trans2@test.com',
                      password_hash=generate_password_hash('123456'), role='translator')
        trans3 = User(name='Phạm Thị Dung', email='trans3@test.com',
                      password_hash=generate_password_hash('123456'), role='translator')
        trans4 = User(name='Hoàng Minh Đức', email='trans4@test.com',
                      password_hash=generate_password_hash('123456'), role='translator')

        db.session.add_all([admin, hirer1, hirer2, trans1, trans2, trans3, trans4])
        db.session.commit()

        # === TRANSLATOR PROFILES ===
        prof1 = TranslatorProfile(
            user_id=trans1.id,
            title='Chuyên gia phiên dịch tiếng Nhật (JLPT N1)',
            bio='Tôi có 7 năm kinh nghiệm phiên dịch cabin và tháp tùng cho các tập đoàn Nhật Bản tại Việt Nam. Từng phiên dịch cho Toyota, Honda, Fujitsu.',
            languages='Tiếng Nhật, Tiếng Anh',
            badges='Rising Star, Local Champion',
            rating=4.8, total_reviews=25, total_jobs=30, is_verified=True
        )
        prof2 = TranslatorProfile(
            user_id=trans2.id,
            title='Biên/Phiên dịch viên tiếng Anh - Pháp chuyên ngành pháp lý',
            bio='Thạc sĩ Luật quốc tế, có 5 năm dịch hợp đồng, tài liệu pháp lý và phiên dịch hội thảo cho các tổ chức quốc tế.',
            languages='Tiếng Anh, Tiếng Pháp',
            badges='Rehire Badge',
            rating=4.6, total_reviews=18, total_jobs=22, is_verified=True
        )
        prof3 = TranslatorProfile(
            user_id=trans3.id,
            title='Phiên dịch viên tiếng Hàn (TOPIK 6) - Chuyên ngành kỹ thuật',
            bio='6 năm làm việc tại Hàn Quốc, chuyên dịch hội nghị kỹ thuật, nhà máy sản xuất Samsung, LG.',
            languages='Tiếng Hàn, Tiếng Anh',
            badges='Local Champion',
            rating=4.9, total_reviews=42, total_jobs=55, is_verified=True
        )
        prof4 = TranslatorProfile(
            user_id=trans4.id,
            title='Phiên dịch tiếng Trung - Tiếng Đức đa lĩnh vực',
            bio='Tốt nghiệp HSK 6 và tiếng Đức C1. Có kinh nghiệm dịch thương mại và du lịch.',
            languages='Tiếng Trung, Tiếng Đức',
            badges='Rising Star',
            rating=4.3, total_reviews=8, total_jobs=10, is_verified=False
        )

        db.session.add_all([prof1, prof2, prof3, prof4])
        db.session.commit()

        # === SERVICES ===
        services = [
            Service(profile_id=prof1.id, name='Phiên dịch tháp tùng tiếng Nhật',
                    description='Đi cùng đoàn khách Nhật tại sự kiện, hội nghị, thăm quan nhà máy.',
                    category='Tháp tùng', languages='Việt ↔ Nhật',
                    basic_price=1500000, standard_price=2500000, premium_price=4000000,
                    basic_delivery='1 ngày', standard_delivery='Nửa ngày', premium_delivery='Theo yêu cầu'),
            Service(profile_id=prof1.id, name='Biên dịch tài liệu tiếng Nhật',
                    description='Dịch hợp đồng, email, tài liệu kỹ thuật Nhật-Việt.',
                    category='Dịch viết', languages='Việt ↔ Nhật',
                    basic_price=300000, standard_price=500000, premium_price=900000,
                    basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
            Service(profile_id=prof2.id, name='Phiên dịch cabin hội thảo tiếng Anh',
                    description='Dịch cabin đồng thời trong hội nghị quốc tế, đảm bảo tốc độ và chính xác.',
                    category='Cabin', languages='Việt ↔ Anh',
                    basic_price=3000000, standard_price=4500000, premium_price=7000000,
                    basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
            Service(profile_id=prof3.id, name='Phiên dịch hội nghị tiếng Hàn',
                    description='Dịch hội nghị kỹ thuật, đào tạo nội bộ, meeting doanh nghiệp Hàn Quốc.',
                    category='Hội nghị', languages='Việt ↔ Hàn',
                    basic_price=2000000, standard_price=3200000, premium_price=5000000,
                    basic_delivery='Theo lịch', standard_delivery='Theo lịch', premium_delivery='Theo lịch'),
            Service(profile_id=prof4.id, name='Biên dịch tiếng Trung chuyên ngành thương mại',
                    description='Dịch hợp đồng thương mại, catalogue sản phẩm, email kinh doanh.',
                    category='Dịch viết', languages='Việt ↔ Trung',
                    basic_price=250000, standard_price=400000, premium_price=700000,
                    basic_delivery='3 ngày', standard_delivery='2 ngày', premium_delivery='Trong ngày'),
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

        db.session.add_all([job1, job2, job3])
        db.session.commit()

        # === PROPOSALS ===
        p1 = Proposal(job_id=job1.id, translator_id=trans1.id,
                      cover_letter='Tôi có 7 năm dịch cabin/tháp tùng IT tiếng Nhật cho Fujitsu và FPT. Rất hân hạnh được hợp tác!',
                      price=2800000, time_estimate='1 ngày', status='accepted')
        p2 = Proposal(job_id=job2.id, translator_id=trans2.id,
                      cover_letter='Thạc sĩ luật quốc tế, đã dịch hơn 100 bộ hợp đồng thương mại Mỹ - Việt.',
                      price=700000, time_estimate='2 ngày', status='pending')
        p3 = Proposal(job_id=job3.id, translator_id=trans3.id,
                      cover_letter='TOPIK 6, 6 năm làm việc tại Hàn Quốc và dịch cho các dự án Samsung Display.',
                      price=6500000, time_estimate='3 ngày', status='pending')
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        # === CONTRACTS (Phòng làm việc trực tiếp) ===
        # Contract 1: In Progress - Hội thảo IT Nhật (Job 1)
        c1 = Contract(
            job_id=job1.id,
            proposal_id=p1.id,
            hirer_id=hirer1.id,
            translator_id=trans1.id,
            agreed_price=2800000,
            scheduled_date='2026-09-22',
            scheduled_time_start='08:00',
            scheduled_time_end='17:00',
            location='FPT Tower, Quận 7, TP.HCM',
            status='in_progress'
        )

        # Contract 2: Escrow Pending - Dịch vụ Tiếng Anh (Service 3)
        c2 = Contract(
            service_id=services[2].id,
            hirer_id=hirer1.id,
            translator_id=trans2.id,
            agreed_price=3000000,
            scheduled_date='2026-09-26',
            scheduled_time_start='09:00',
            scheduled_time_end='12:00',
            location='Trung tâm Hội nghị GEM Center, Q1, TP.HCM',
            status='escrow_pending'
        )

        # Contract 3: Completed - Dịch vụ Tiếng Hàn (Service 4)
        c3 = Contract(
            service_id=services[3].id,
            hirer_id=hirer2.id,
            translator_id=trans3.id,
            agreed_price=2000000,
            scheduled_date='2026-09-10',
            scheduled_time_start='13:30',
            scheduled_time_end='17:30',
            location='Khách sạn Lotte, Hà Nội',
            status='completed'
        )

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # === MESSAGES & DELIVERABLES FOR CONTRACT 1 ===
        m1 = Message(contract_id=c1.id, sender_id=hirer1.id,
                     content='Chào bạn Bích, rất vui được hợp tác cùng bạn trong buổi hội thảo IT sắp tới!')
        m2 = Message(contract_id=c1.id, sender_id=trans1.id,
                     content='Dạ em chào anh An! Em đã nhận thông tin và đang chuẩn bị sẵn bộ thuật ngữ chuyên ngành IT cho buổi hội thảo.')
        m3 = Message(contract_id=c1.id, sender_id=hirer1.id,
                     content='Tuyệt vời, anh đã nộp tiền ký quỹ Escrow rồi nhé. Em gửi file tài liệu tham khảo khi chuẩn bị xong nhé.')
        m4 = Message(contract_id=c1.id, sender_id=trans1.id,
                     content='Dạ vâng anh, em gửi bản tổng hợp thuật ngữ và slide dịch nháp qua phòng làm việc đây ạ.')

        d1 = Deliverable(contract_id=c1.id, filename='Glossary_IT_Ja_Vi.docx', filepath='Glossary_IT_Ja_Vi.docx')
        db.session.add_all([m1, m2, m3, m4, d1])

        # === REVIEW FOR CONTRACT 3 ===
        r1 = Review(contract_id=c3.id, reviewer_id=hirer2.id, reviewee_id=trans3.id,
                    rating=5, comment='Chị Dung phiên dịch rất trôi chảy, phản xạ nhanh và tác phong vô cùng chuyên nghiệp. Nhất định sẽ tiếp tục hợp tác!')
        db.session.add(r1)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print('Seeded successfully with rich contracts & workspace data!')
