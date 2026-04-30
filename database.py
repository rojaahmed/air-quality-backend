import psycopg2
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL")
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