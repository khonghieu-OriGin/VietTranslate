import os
import sys

# Thêm thư mục gốc vào sys.path để Vercel có thể tìm thấy app.py và các module khác
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
