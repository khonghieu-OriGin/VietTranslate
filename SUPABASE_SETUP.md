# Hướng dẫn Kết nối Supabase

## 1. Tạo Supabase Project

1. Truy cập [supabase.com](https://supabase.com) và đăng nhập
2. Nhấp **New Project**
3. Điền thông tin:
   - **Project Name**: `viettranslate` (hoặc tên tùy chọn)
   - **Database Password**: Tạo mật khẩu mạnh
   - **Region**: Chọn region gần nhất (ví dụ: Singapore)
4. Nhấp **Create new project** và chờ dự án khởi tạo

## 2. Lấy Supabase Credentials

Sau khi project tạo xong, vào phần **Settings** → **API**:

- **Project URL**: `https://your-project.supabase.co`
- **Anon Public Key**: Public key dùng cho client-side
- **Service Role Key**: Secret key chỉ dùng server-side (GIỮ RIÊNG TƯ)

## 3. Cấu hình Environment Variables

1. Tạo file `.env` từ template:
```bash
cp .env.example .env
```

2. Cập nhật các biến:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_DB_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
```

3. **Quan trọng**: Lấy PostgreSQL connection string:
   - Vào **Settings** → **Database** → **Connection Info**
   - Copy URI ở mục **Connection string** (URI pattern)
   - Thay `[YOUR-PASSWORD]` bằng password bạn tạo ở bước 1

## 4. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## 5. Tạo Bảng Dữ liệu

### Cách 1: Dùng Supabase SQL Editor (Khuyến nghị cho lần đầu)

Vào **SQL Editor** trong Supabase Dashboard và chạy các query để tạo tables tương ứng với models trong `models.py`.

### Cách 2: Tự động tạo từ SQLAlchemy (Tùy chọn)

```python
from app import app, db
with app.app_context():
    db.create_all()
```

## 6. Migration (Nếu cần)

Nếu dùng Flask-Migrate:

```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 7. Test Kết nối

```bash
python supabase_client.py
```

Bạn sẽ thấy:
- ✓ Kết nối Supabase thành công!
- hoặc ✗ Lỗi (nếu có vấn đề)

## 8. Cấu hình Production (Vercel)

### Thêm Environment Variables trong Vercel Dashboard:

1. Vào **Settings** → **Environment Variables**
2. Thêm:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_DB_URL`
   - `FLASK_ENV=production`

### Deploy:
```bash
git push  # Vercel tự động deploy
```

## 9. Cẩn Thận

⚠️ **Bảo mật:**
- ❌ KHÔNG commit `.env` file (được ignore trong `.gitignore`)
- ❌ KHÔNG chia sẻ `SUPABASE_DB_URL` hoặc service role keys
- ✅ CHỈ dùng anon public key cho client-side
- ✅ Dùng service role key chỉ trong backend code

## 10. Tham Khảo

- [Supabase Docs](https://supabase.com/docs)
- [SQLAlchemy + PostgreSQL](https://docs.sqlalchemy.org/en/20/)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)

## Lỗi Thường Gặp

### "SUPABASE_URL or SUPABASE_KEY not configured"
→ Kiểm tra `.env` file có các biến không

### "Connection refused" hoặc "timeout"
→ Kiểm tra `SUPABASE_DB_URL` đúng chưa
→ Kiểm tra network/firewall có chặn không

### "Table does not exist"
→ Chạy SQL migrations trong Supabase SQL Editor
→ Hoặc gọi `db.create_all()` trong Flask shell

---

**Bạn đã sẵn sàng!** Dự án giờ kết nối với Supabase PostgreSQL. 🚀
