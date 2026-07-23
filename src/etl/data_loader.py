import sqlite3
from pathlib import Path

import pandas as pd

from src.etl.normaliser import normalize_dataframe

DB_PATH = Path("db/nifty100.db")

FILES = {
    "companies": ("companies.xlsx", 1),
    "balancesheet": ("balancesheet.xlsx", 1),
    "profitandloss": ("profitandloss.xlsx", 1),
    "cashflow": ("cashflow.xlsx", 1),
    "analysis": ("analysis.xlsx", 1),
    "documents": ("documents.xlsx", 1),
    "prosandcons": ("prosandcons.xlsx", 1),
    "financial_ratios": ("financial_ratios.xlsx", 0),
    "market_cap": ("market_cap.xlsx", 0),
    "peer_groups": ("peer_groups.xlsx", 0),
    "sectors": ("sectors.xlsx", 0),
    "stock_prices": ("stock_prices.xlsx", 0)
}

def load_dataset(file_name, header):
    path = Path("data/raw") / file_name

    df = pd.read_excel(path, header=header)

    df = normalize_dataframe(df)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    return df

def insert_table(conn, table_name, df):
    try:
        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )
        print(f"✓ {table_name} loaded successfully ({len(df)} rows)")

    except Exception as e:
        print("\n===================================")
        print(f"Error while loading: {table_name}")
        print(type(e))
        print(e)

        if hasattr(e, "__cause__") and e.__cause__:
            print("\nActual SQLite Error:")
            print(type(e.__cause__))
            print(e.__cause__)

        print("===================================\n")
        raise

    print(f"{table_name} loaded ({len(df)} rows)")
    
def load_all_data():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")

    companies_df = load_dataset("companies.xlsx", 1)
    valid_ids = set(companies_df["id"].astype(str).str.strip())

    for table, (file, header) in FILES.items():
        print(f"\nLoading {table}...")

        df = load_dataset(file, header)

        if table != "companies" and "company_id" in df.columns:
            before = len(df)

            df["company_id"] = df["company_id"].astype(str).str.strip()
            df = df[df["company_id"].isin(valid_ids)]

            skipped = before - len(df)

            if skipped > 0:
                print(f"⚠ Skipped {skipped} invalid rows from {table}")

        try:
            insert_table(conn, table, df)
            print(f"✓ {table} loaded successfully")

        except Exception as e:
            print(f"✗ Error loading {table}")
            print(e)
            break

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    load_all_data()