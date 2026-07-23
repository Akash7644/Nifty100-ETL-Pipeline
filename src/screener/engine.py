import sqlite3
from pathlib import Path

import pandas as pd
import yaml

DB_PATH = Path("db/nifty100.db")
CONFIG_PATH = Path("config/screener_config.yaml")


def load_financial_ratios():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )
    conn.close()
    return df


def load_config():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)
    return config["filters"]


def apply_filters(df, filters):
    filtered = df.copy()

    # ROE
    if filters["roe_min"] is not None:
        filtered = filtered[
            filtered["return_on_equity_pct"] >= filters["roe_min"]
        ]

    # Revenue CAGR
    if filters["revenue_cagr_5yr_min"] is not None:
        filtered = filtered[
            filtered["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]
        ]

    # PAT CAGR
    if filters["pat_cagr_5yr_min"] is not None:
        filtered = filtered[
            filtered["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]
        ]

    # EPS CAGR
    if filters["eps_cagr_5yr_min"] is not None:
        filtered = filtered[
            filtered["eps_cagr_5yr"] >= filters["eps_cagr_5yr_min"]
        ]

    # Operating Profit Margin
    if filters["operating_profit_margin_min"] is not None:
        filtered = filtered[
            filtered["operating_profit_margin_pct"]
            >= filters["operating_profit_margin_min"]
        ]

    # Asset Turnover
    if filters["asset_turnover_min"] is not None:
        filtered = filtered[
            filtered["asset_turnover"] >= filters["asset_turnover_min"]
        ]

    # Debt to Equity (Excluding Financials)
    if filters["debt_to_equity_max"] is not None:
        financials = filtered[filtered["broad_sector"] == "Financials"]
        others = filtered[filtered["broad_sector"] != "Financials"]
        others = others[others["debt_to_equity"] <= filters["debt_to_equity_max"]]
        filtered = pd.concat([financials, others], ignore_index=True)

    # Interest Coverage Ratio
    if filters["interest_coverage_min"] is not None:
        debt_free = filtered[filtered["icr_label"] == "Debt Free"]
        others = filtered[filtered["icr_label"] != "Debt Free"]
        others = others[
            others["interest_coverage"] >= filters["interest_coverage_min"]
        ]
        filtered = pd.concat([debt_free, others], ignore_index=True)

    # Composite Score
    filtered["composite_quality_score"] = 0
    filtered = filtered.sort_values(
        "composite_quality_score",
        ascending=False,
    )

    return filtered


if __name__ == "__main__":
    ratios = load_financial_ratios()
    config = load_config()
    screened = apply_filters(ratios, config)

    print("\nScreening Complete")
    print(f"Companies Found: {len(screened)}")
    print(
        screened[
            [
                "company_name",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "composite_quality_score",
            ]
        ].head(20)
    )
