import sqlite3
import pandas as pd
from pathlib import Path

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)

DB_PATH = Path("db/nifty100.db")


def load_tables():
    conn = sqlite3.connect(DB_PATH)

    profit = pd.read_sql("SELECT * FROM profitandloss", conn)
    balance = pd.read_sql("SELECT * FROM balancesheet", conn)
    companies = pd.read_sql("SELECT * FROM companies", conn)

    conn.close()

    return profit, balance, companies

def prepare_data():
    profit, balance, companies = load_tables()

    df = profit.merge(
        balance,
        on=["company_id", "year"],
        how="inner",
        suffixes=("_pl", "_bs"),
    )

    df = df.merge(
        companies[["id", "company_name", "roce_percentage", "roe_percentage"]],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    return df

def compute_profitability(df):
    results = []

    for _, row in df.iterrows():

        opm, opm_match = operating_profit_margin(
            row["operating_profit"],
            row["sales"],
            row["opm_percentage"],
        )

        roe = return_on_equity(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"],
        )

        roce = return_on_capital_employed(
            row["operating_profit"]
            + row["interest"]
            + row["depreciation"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"],
        )

        roa = return_on_assets(
            row["net_profit"],
            row["total_assets"],
        )

        npm = net_profit_margin(
            row["net_profit"],
            row["sales"],
        )

        results.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],
                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,
                "opm_match": opm_match,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,
            }
        )

    return pd.DataFrame(results)

if __name__ == "__main__":
    data = prepare_data()

    ratios = compute_profitability(data)

    print(ratios.head())