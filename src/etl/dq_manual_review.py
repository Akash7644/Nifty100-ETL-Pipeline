import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------
# 5 Random Companies Review
# -----------------------------

companies = pd.read_sql_query(
    "SELECT id, company_name FROM companies",
    conn
)

sample = companies.sample(n=5, random_state=42)

print("=" * 70)
print("DATA QUALITY MANUAL REVIEW - 5 RANDOM COMPANIES")
print("=" * 70)

for _, row in sample.iterrows():

    company_id = row["id"]
    company_name = row["company_name"]

    print(f"\nCompany Name : {company_name}")
    print(f"Company ID   : {company_id}")

    years = pd.read_sql_query(
        """
        SELECT DISTINCT year
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    if years.empty:
        print("Balance Sheet Data : Not Available")
    else:
        print("Available Years    :", years["year"].tolist())
        print("Total Years        :", len(years))

# -----------------------------
# Companies with < 5 years
# -----------------------------

print("\n" + "=" * 70)
print("COMPANIES WITH LESS THAN 5 YEARS OF DATA")
print("=" * 70)

query = """
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available
FROM balancesheet
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5
ORDER BY years_available, company_id;
"""

df = pd.read_sql_query(query, conn)

if df.empty:
    print("All companies have at least 5 years of Balance Sheet data.")
else:
    print(df.to_string(index=False))

conn.close()