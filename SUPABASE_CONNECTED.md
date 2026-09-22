# ✅ Supabase Connection - Hoàn Tất Setup

## 📋 Tình Trạng Hiện Tại

- ✅ Project Supabase: **viettranslate Project**
- ✅ URL: `https://ernfqcdpqvjyawbcjgzi.supabase.co`
- ✅ Database: Southeast Asia (Singapore)
- ✅ Environment variables: `.env` file đã tạo
- ✅ app.py: Đã cập nhật để hỗ trợ Supabase

---

## 🚀 Các Bước Cần Làm NGAY

### 1. **Chạy SQL Script Trong Supabase** (QUAN TRỌNG!)

Đây là bước **KHÔNG SKIP** được:

1. Vào **Supabase Dashboard** → https://supabase.com/dashboard
2. Chọn project **viettranslate Project**
3. Click **SQL Editor** (bên trái)
4. Click **New Query**
5. Mở file `supabase_migrations.sql` từ project
6. Copy **toàn bộ nội dung** của file
7. Paste vào SQL Editor ✏️
8. Click nút **RUN** (hoặc Ctrl+Enter)

✅ Khi chạy xong, bạn sẽ thấy **12 bảng dữ liệu** được tạo:
- `user` - Người dùng
- `translator_profile` - Hồ sơ phiên dịch viên
- `job` - Công việc phiên dịch
- `proposal` - Đề xuất/báo giá
- `contract` - Hợp đồng
- ... và các bảng khác

---

### 2. **Cài Đặt Dependencies Trên Máy Tính**

```bash
pip install -r requirements.txt
```

Các package sẽ được cài:
- `flask==3.0.0`
- `flask-sqlalchemy==3.1.1`
- `supabase==2.3.1` ✨ MỚI
- `python-dotenv==1.0.0` ✨ MỚI
- ... và các package khác

---

### 3. **Test Kết Nối Supabase** (Tùy chọn)

```bash
python supabase_client.py
```

Bạn sẽ thấy output:
```
✓ Kết nối Supabase thành công!
```

Hoặc nếu có lỗi:
```
✗ Lỗi kết nối Supabase: ...
```

---

### 4. **Chạy Flask App**

```bash
python app.py
```

Khi chạy, bạn sẽ thấy:
```
[✓] Database: Supabase
 * Running on http://127.0.0.1:5000
```

---

## 📁 Files Được Tạo/Cập Nhật

### Tạo Mới:
- ✨ `.env` - Environment variables (KHÔNG commit lên Git)
- ✨ `.env.example` - Template cho .env
- ✨ `config.py` - Configuration management
- ✨ `supabase_client.py` - Supabase client wrapper
- ✨ `supabase_migrations.sql` - SQL script để tạo tables
- ✨ `SUPABASE_SETUP.md` - Hướng dẫn setup
- ✨ `INTEGRATION_GUIDE.md` - Ví dụ code integration
- ✨ `SUPABASE_CONNECTED.md` - File này

### Cập Nhật:
- 🔄 `app.py` - Thêm import config, support Supabase
- 🔄 `requirements.txt` - Thêm supabase + python-dotenv
- 🔄 `.gitignore` - Ignore .env files (bảo mật)

---

## 🔑 Credentials Đã Lưu Trong `.env`

```env
SUPABASE_URL=https://ernfqcdpqvjyawbcjgzi.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_DB_URL=postgresql://postgres:Huyen271%40%23%24@db.ernfqcdpqvjyawbcjgzi.supabase.co:5432/postgres
```

⚠️ **GIỮ BÍ MẬT**: Đừng chia sẻ file `.env`!

---

## 📊 Database Schema

Đã tạo **12 bảng** tương ứng với models.py:

```
Users
├── user (người dùng)
├── translator_profile (hồ sơ phiên dịch viên)
├── translator_preference (sở thích phiên dịch)
└── service (dịch vụ)

Jobs & Proposals
├── job (công việc phiên dịch)
├── proposal (đề xuất/báo giá)
└── contract (hợp đồng)

Communication
├── message (tin nhắn)
└── direct_message (tin nhắn trực tiếp)

Deliverables & Reviews
├── deliverable (sản phẩm giao dịch)
├── review (đánh giá)
└── notification (thông báo)
```

---

## ✅ Kiểm Tra Setup

### Cách 1: Kiểm Tra .env File

```bash
cat .env
```

Đảm bảo có những biến:
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_KEY`
- ✅ `SUPABASE_DB_URL`

### Cách 2: Kiểm Tra Database Tables

Vào **Supabase Dashboard** → **Table Editor**, bạn sẽ thấy tất cả 12 bảng

### Cách 3: Chạy Test Connection

```bash
python supabase_client.py
```

---

## 🎯 Tiếp Theo (Tùy Chọn)

1. **Seed Data** - Thêm dữ liệu test vào database
   ```bash
   python seed_data.py  # Nếu file này tồn tại
   ```

2. **Migrate MongoDB → Supabase** - Nếu muốn chuyển dữ liệu cũ
   - Xem hướng dẫn trong `INTEGRATION_GUIDE.md`

3. **Real-time Subscriptions** - Dùng Supabase real-time API
   - Thêm code trong app.py để subscribe to changes

4. **Row Level Security (RLS)** - Bảo mật dữ liệu
   - Cấu hình trong Supabase Dashboard

---

## 🆘 Troubleshooting

### Lỗi: "relation does not exist"
```
psycopg.errors.UndefinedTable: relation "user" does not exist
```
→ Chưa chạy SQL script. Làm lại **Bước 1**

### Lỗi: "SUPABASE_DB_URL invalid"
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URI
```
→ Kiểm tra password có ký tự đặc biệt không. Cần URL-encode:
- `@` → `%40`
- `#` → `%23`
- `$` → `%24`
- `%` → `%25`

### Lỗi: "Connection refused"
```
sqlalchemy.exc.OperationalError: could not connect to server
```
→ Kiểm tra SUPABASE_DB_URL chính xác chưa
→ Kiểm tra network/firewall

### Lỗi: "no such module 'dotenv'"
```
ModuleNotFoundError: No module named 'dotenv'
```
→ Chưa cài dependencies:
```bash
pip install -r requirements.txt
```

---

## 📞 Support

Nếu có vấn đề:
1. Kiểm tra `.env` file có đúng không
2. Kiểm tra SQL tables được tạo trong Supabase chưa
3. Kiểm tra `pip install -r requirements.txt` đã chạy chưa
4. Xem `SUPABASE_SETUP.md` để có hướng dẫn chi tiết

---

**Status: ✅ SUPABASE CONNECTED** 🎉

Giờ app.py đã sẵn sàng để sử dụng Supabase PostgreSQL!
