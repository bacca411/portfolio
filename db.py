import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", "data/portfolio.db")

def ensure_db_folder():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    ensure_db_folder()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS training_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        minutes INTEGER NOT NULL,
        notes TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()