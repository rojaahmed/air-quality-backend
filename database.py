import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://air_quality_db_ot1x_user:rFUy0TGz73uEbwZ1f2JQXgEltAKjrtva@dpg-d5c1moje5dus7383fqdg-a.virginia-postgres.render.com:5432/air_quality_db_ot1x"

@contextmanager
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()  # commit işlemi yield sonrası
    except Exception as e:
        conn.rollback()  # hata olursa geri al
        raise e
    finally:
        cursor.close()
        conn.close()
