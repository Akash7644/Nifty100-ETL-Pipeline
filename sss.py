import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

# Check if the table exists
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print("Tables in Database:")
print(tables)

print("\n" + "="*60)

# Check financial_ratios table
try:
    df = pd.read_sql(
        "SELECT * FROM financial_ratios LIMIT 10;",
        conn
    )

    print("financial_ratios table exists.\n")
    print(df)

    print("\nColumns:")
    print(df.columns.tolist())

    total = pd.read_sql(
        "SELECT COUNT(*) AS total_records FROM financial_ratios;",
        conn
    )

    print("\nTotal Records:")
    print(total)

except Exception as e:
    print("Error:", e)

conn.close()