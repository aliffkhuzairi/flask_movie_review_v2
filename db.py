import psycopg2, os
from contextlib import contextmanager

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'),
    )

@contextmanager
def db_cursor(commit=False):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        yield cur
        if commit:
            conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()