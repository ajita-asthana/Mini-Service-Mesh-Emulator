import sqlite3


def get_connection():
    return sqlite3.connect("service_mesh.db")


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            status TEXT
        )
        """)
        conn.commit()
