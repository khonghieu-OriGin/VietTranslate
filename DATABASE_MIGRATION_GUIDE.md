# Hướng Dẫn Migration Cập Nhật Schema Production

## Vấn Đề Hiện Tại
Code `models.py` mới đã được deploy nhưng database PostgreSQL production (trên Supabase) chưa được cập nhật schema tương ứng. Điều này gây ra lỗi 500 khi ứng dụng chạy (ví dụ: `psycopg.errors.UndefinedColumn: column user.admin_role does not exist`), vì SQLAlchemy cố gắng query các column chưa tồn tại.

Đặc biệt, hệ thống sử dụng **Admin Shell** mới và **Chống Trùng Lịch**, dẫn đến nhiều column mới được thêm vào.

---

## 1. Các Migration Đã Có
Dưới đây là các script SQL bạn cần thực thi để đồng bộ schema:

1. `migration_sync_current_schema.sql` (Vừa tạo) - Thêm toàn bộ các column mới cho bảng `user` và `translator_schedule`, cũng như tự động tạo các bảng mới (nếu chưa có).
2. `migration_add_expires_at.sql` (Cũ, đã gộp vào script 1)
3. `migration_add_exclusion.sql` (Cũ, đã được an toàn hóa và gộp vào script 1 bằng DO BLOCK).

**Bạn CHỈ CẦN chạy file `migration_sync_current_schema.sql`** là đủ. Script này được viết an toàn (idempotent), có chứa `IF NOT EXISTS` để không báo lỗi hay xóa đè dữ liệu cũ.

---

## 2. Các Bước Thực Hiện Migration trên Supabase

**LƯU Ý QUAN TRỌNG:** KHÔNG DÙNG `db.create_all()` từ local để update schema của production database, vì `create_all()` không thể thêm column vào bảng đã tồn tại!

**Bước 1: Mở Supabase SQL Editor**
- Đăng nhập vào Supabase Dashboard.
- Chọn Project của bạn.
- Ở menu bên trái, chọn **SQL Editor**.

**Bước 2: Chạy Migration Script**
- Chọn "New Query".
- Copy toàn bộ nội dung từ file `migration_sync_current_schema.sql`.
- Dán vào SQL Editor.
- Bấm **Run**.
- Đợi dòng thông báo `Success. No rows returned.` hiện lên.

**Bước 3: Xác minh (Verification)**
Sau khi chạy, bạn có thể thực hiện 2 cách kiểm tra:
1. **Qua Vercel/Website:** Thử truy cập trang web (đặc biệt các route `/admin/*` và trang của phiên dịch viên). Lỗi `UndefinedColumn` 500 sẽ không còn.
2. **Qua SQL Editor:** Chạy các query sau để xác nhận:
   ```sql
   SELECT admin_role, is_admin, is_active FROM "user" LIMIT 5;
   SELECT buffer_before_minutes, buffer_after_minutes, expires_at FROM translator_schedule LIMIT 5;
   ```
   Nếu query chạy bình thường, chúc mừng! Schema đã được đồng bộ.

---

## 3. Cách Hoạt Động của Admin Role Sau Migration
- Cột `admin_role` được thiết lập mặc định là `NULL` (không bắt buộc).
- `is_admin` mặc định là `FALSE`.
- Điều này đảm bảo:
  - Tài khoản người dùng cũ vẫn hoạt động bình thường (không bị lỗi).
  - Không ai tự nhiên trở thành Admin khi schema mới được áp dụng.
  - Phải được gán quyền chủ động (qua script seed_data hoặc backend) mới truy cập được `/admin/*`.
  - Backend đã kiểm tra `is_admin` trực tiếp qua Database, ngăn chặn việc bypass qua front-end.

---

## 4. Rollback (Khôi Phục) Nếu Cần
Nếu migration có vấn đề (do lỗi logic hoặc đổi ý), bạn có thể gỡ bỏ các cột vừa thêm bằng các lệnh sau trên SQL Editor:

```sql
-- CHỈ DÙNG KHI THỰC SỰ CẦN THIẾT! SẼ LÀM MẤT QUYỀN ADMIN.
ALTER TABLE "user" 
DROP COLUMN IF EXISTS admin_role,
DROP COLUMN IF EXISTS is_admin,
DROP COLUMN IF EXISTS is_active;

ALTER TABLE translator_schedule
DROP COLUMN IF EXISTS buffer_before_minutes,
DROP COLUMN IF EXISTS buffer_after_minutes,
DROP COLUMN IF EXISTS status,
DROP COLUMN IF EXISTS expires_at;

ALTER TABLE translator_schedule
DROP CONSTRAINT IF EXISTS no_overlapping_schedules;
```

---

## 5. Tóm Tắt Code Đã Fix
1. **Lỗi ngầm khi thiếu column:** Đã cập nhật `app.py`, sửa hàm `_init_db()` để thực hiện 1 query thử (`dummy_user = db.session.query(User).first()`). Giờ đây, nếu backend khởi động mà thiếu column, hệ thống sẽ **in log đỏ rõ ràng** `DATABASE SCHEMA DRIFT DETECTED` trên Vercel thay vì ỉm đi và chết ngầm.
2. **Ngăn fallback về In-memory DB:** Vercel giờ đây BẮT BUỘC phải có `DATABASE_URL` hoặc `MONGO_URI`. Không còn tình trạng website tự tạo DB SQLite in-memory, chạy bình thường nhưng mất sạch dữ liệu sau 1 giờ.
3. **Script kiểm tra:** Bạn có thể chạy `python scripts/check_schema.py` ở local (trỏ `DATABASE_URL` về production) để kiểm tra thiếu table/column tự động mà không cần vào Supabase.
