import pyodbc
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=HavaKalitesiProje1;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()
