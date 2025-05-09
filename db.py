import sqlite3

DB_PATH = "sinfomik.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siswa (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nisn INTEGER NOT NULL,
                nama TEXT NOT NULL
            )
        ''')
        conn.commit()