import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS financial_ratios (

    company_id TEXT NOT NULL,
    year TEXT NOT NULL,

    company_name TEXT,
    broad_sector TEXT,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    opm_match BOOLEAN,

    return_on_equity_pct REAL,
    return_on_capital_employed_pct REAL,
    return_on_assets_pct REAL,

    debt_to_equity REAL,
    high_leverage_flag BOOLEAN,

    interest_coverage REAL,
    icr_label TEXT,
    interest_warning BOOLEAN,

    net_debt REAL,
    asset_turnover REAL,

    revenue_cagr_5yr REAL,
    revenue_cagr_5yr_flag TEXT,

    pat_cagr_5yr REAL,
    pat_cagr_5yr_flag TEXT,

    eps_cagr_5yr REAL,
    eps_cagr_5yr_flag TEXT,

    operating_activity_ratio REAL,
    investing_activity_ratio REAL,
    financing_activity_ratio REAL,

    net_cash_flow_margin REAL,
    cash_flow_flag TEXT,

    PRIMARY KEY(company_id, year)
)
""")

conn.commit()
conn.close()

print("financial_ratios table created successfully.")