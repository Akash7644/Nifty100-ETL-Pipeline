import sqlite3

from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def test_financial_ratio_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    )

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 0