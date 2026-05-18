import psycopg2, os
from contextlib import contextmanager

def get_db_connection():
    host = os.getenv('DATABASE_HOST', 'localhost')
    sslmode = 'require' if 'neon.tech' in host else 'disable'

    return psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=host,
        port=os.getenv('DATABASE_PORT'),
        sslmode=sslmode
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