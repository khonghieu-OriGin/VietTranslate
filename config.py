import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    PRIVATE_STORAGE_FOLDER = os.getenv('PRIVATE_STORAGE_FOLDER', os.path.join('instance', 'storage', 'private_verifications'))
    
    # Mail Config
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@viettranslate.com')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///instance/database.db'
    )

class ProductionConfig(Config):
    """Production configuration — Supabase PostgreSQL only."""
    DEBUG = False

    # Supabase PostgreSQL—primary database
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL')

    # DATABASE_URL takes priority; SUPABASE_DB_URL is a documented alias.
    # TASK 11: Không fallback SQLite. Nếu thiếu → app sẽ raise RuntimeError khi khởi động.
    _db_url = os.getenv('DATABASE_URL') or os.getenv('SUPABASE_DB_URL')
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        # Fallback — sẽ bị ghi đè bởi logic fail-fast trong app.py nếu chạy trên Vercel/Render
        SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }

    return config_map.get(env, DevelopmentConfig)
