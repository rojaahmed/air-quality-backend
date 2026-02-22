import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres.lgfomuqhuyehqbrwmwoq:Rojda45670%2A%25@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"

@contextmanager
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()