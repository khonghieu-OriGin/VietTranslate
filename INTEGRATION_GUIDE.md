# Hướng Dẫn Tích Hợp Supabase vào app.py

## Cách Cập Nhật app.py Để Dùng Supabase

### Bước 1: Import Config

Thêm những import này ở đầu `app.py`:

```python
from dotenv import load_dotenv
from config import get_config
from supabase_client import supabase

load_dotenv()
```

### Bước 2: Thay Thế Phần Khởi Tạo

Tìm phần này trong `app.py`:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
basedir = os.path.abspath(os.path.dirname(__file__))
database_url = os.getenv("DATABASE_URL")
if not database_url:
    database_url = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

Và thay bằng:

```python
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Khởi tạo database từ config
database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
if not database_url:
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_url = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```

### Bước 3: Thêm Supabase Initialization (Optional)

Để sử dụng Supabase client cho queries không dùng SQLAlchemy:

```python
# Sau app.config setup
if supabase:
    print("[✓] Supabase client đã sẵn sàng")
else:
    print("[!] Supabase chưa được cấu hình, dùng SQLAlchemy")
```

## Ví Dụ Sử Dụng Supabase

### 1. Dùng SQLAlchemy (Recommended cho ORM)

```python
from models import db, User

# Tạo user
user = User(
    name="Nguyễn Văn A",
    email="a@example.com",
    password_hash=generate_password_hash("password"),
    phone="0912345678",
    role="translator"
)
db.session.add(user)
db.session.commit()

# Tìm user
user = User.query.filter_by(email="a@example.com").first()
```

### 2. Dùng Supabase Client (Cho real-time/realtime subscriptions)

```python
from supabase_client import supabase

# Lấy tất cả users
response = supabase.table('users').select('*').execute()
users = response.data

# Tìm user
response = supabase.table('users').select('*').eq('email', 'a@example.com').execute()
user = response.data[0] if response.data else None

# Tạo user (ngoài SQLAlchemy)
response = supabase.table('users').insert({
    'name': 'Nguyễn Văn B',
    'email': 'b@example.com',
    'password_hash': generate_password_hash('password'),
    'role': 'translator'
}).execute()

# Cập nhật user
response = supabase.table('users').update({
    'name': 'Nguyễn Văn C'
}).eq('email', 'b@example.com').execute()

# Xoá user
response = supabase.table('users').delete().eq('email', 'b@example.com').execute()
```

### 3. Real-time Subscriptions (Supabase-specific)

```python
from supabase_client import supabase

# Subscribe to changes
def on_change(payload):
    print(f"Thay đổi: {payload}")

supabase.realtime.on(
    'INSERT',
    lambda x: supabase.table('users').on('*', on_change).subscribe()
)
```

## Migration từ MongoDB sang Supabase

Nếu bạn đang chạy MongoDB hiện tại và muốn chuyển sang Supabase:

### 1. Export dữ liệu từ MongoDB

```python
from pymongo import MongoClient
import json

client = MongoClient(MONGO_URI)
db = client['viettranslate_db']

# Export collections
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    docs = list(collection.find({}))
    with open(f'{collection_name}.json', 'w') as f:
        json.dump(docs, f, default=str)
```

### 2. Tạo tables trong Supabase SQL Editor

Dựa vào structure của collections MongoDB, tạo PostgreSQL tables tương ứng.

### 3. Import dữ liệu vào Supabase

```bash
# Dùng CSV import hoặc script Python
python migrate_to_supabase.py
```

## Troubleshooting

### Lỗi: "no such table: users"
→ Chạy migrations:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Lỗi: "SUPABASE_DB_URL invalid"
→ Kiểm tra connection string format:
```
postgresql://username:password@host:port/database
```

### Lỗi: "relation already exists"
→ Tables đã tồn tại, không cần tạo lại

---

**Sau khi cập nhật xong, chạy:**
```bash
pip install -r requirements.txt
python supabase_client.py  # Test kết nối
```
