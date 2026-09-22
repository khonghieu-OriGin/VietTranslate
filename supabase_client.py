import os
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client():
    """
    Initialize and return Supabase client.
    Returns None if Supabase is not configured.
    """
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        return None

    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        print(f"Lỗi khởi tạo Supabase client: {e}")
        return None

def get_supabase_db_connection():
    """
    Get direct PostgreSQL connection string for SQLAlchemy.
    """
    return os.getenv('SUPABASE_DB_URL')

# Initialize client at module load
supabase = get_supabase_client()

# Example usage functions
def test_supabase_connection():
    """Test Supabase connection"""
    if not supabase:
        print("Supabase chưa được cấu hình")
        return False

    try:
        # Test with a simple query
        response = supabase.table('users').select('id').limit(1).execute()
        print("✓ Kết nối Supabase thành công!")
        return True
    except Exception as e:
        print(f"✗ Lỗi kết nối Supabase: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
