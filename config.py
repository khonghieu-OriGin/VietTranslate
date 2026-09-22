import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///instance/database.db'
    )

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

    # Try Supabase PostgreSQL first
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL')

    if SUPABASE_DB_URL:
        SQLALCHEMY_DATABASE_URI = SUPABASE_DB_URL
    else:
        # Fallback to MongoDB if Supabase not configured
        SQLALCHEMY_DATABASE_URI = os.getenv('MONGO_URI', 'sqlite:///instance/database.db')

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
