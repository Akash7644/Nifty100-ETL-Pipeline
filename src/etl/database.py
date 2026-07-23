import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")


def create_database():
    if DB_PATH.exists():
        DB_PATH.unlink()          # Delete the old database

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("=" * 40)
    print("Database Created Successfully")
    print("=" * 40)
    print(DB_PATH.resolve())


if __name__ == "__main__":
    create_database()