import sqlite3
from pathlib import Path

import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

from src.analytics.cashflow_kpis import (
    operating_activity_ratio,
    investing_activity_ratio,
    financing_activity_ratio,
    net_cash_flow_margin,
    cash_flow_flag,
)

DB_PATH = Path("db/nifty100.db")


def load_tables():
    conn = sqlite3.connect(DB_PATH)

    profit = pd.read_sql("SELECT * FROM profitandloss", conn)
    balance = pd.read_sql("SELECT * FROM balancesheet", conn)
    companies = pd.read_sql("SELECT * FROM companies", conn)
    sectors = pd.read_sql(
        "SELECT company_id, broad_sector FROM sectors",
        conn,
    )
    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    conn.close()

    return profit, balance, companies, sectors, cashflow


def prepare_data():
    profit, balance, companies, sectors, cashflow = load_tables()

    df = profit.merge(
        balance,
        on=["company_id", "year"],
        how="inner",
        suffixes=("_pl", "_bs"),
    )

    df = df.merge(
        companies[
            [
                "id",
                "company_name",
                "roce_percentage",
                "roe_percentage",
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    df = df.merge(
        sectors,
        on="company_id",
        how="left",
    )

    df = df.merge(
        cashflow,
        on=["company_id", "year"],
        how="left",
    )
    return df


def compute_financial_ratios(df):
    results = []
    
    grouped = df.groupby("company_id")
    for company_id, company_data in grouped:
        company_data = company_data.sort_values("year")

        for _, row in company_data.iterrows():

            npm = net_profit_margin(
                row["net_profit"],
                row["sales"],
            )

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

            ebit = (
                row["operating_profit"]
                + row["interest"]
                + row["depreciation"]
            )

            roce = return_on_capital_employed(
                ebit,
                row["equity_capital"],
                row["reserves"],
                row["borrowings"],
            )

            roa = return_on_assets(
                row["net_profit"],
                row["total_assets"],
            )

            de = debt_to_equity(
                row["borrowings"],
                row["equity_capital"],
                row["reserves"],
            )

            high_leverage = high_leverage_flag(
                de,
                row["broad_sector"],
            )

            icr = interest_coverage_ratio(
                row["operating_profit"],
                row["other_income"],
                row["interest"],
            )

            label = icr_label(icr)

            warning = icr_warning_flag(icr)

            nd = net_debt(
                row["borrowings"],
                row["investments"],
            )

            at = asset_turnover(
                row["sales"],
                row["total_assets"],
            )
            
            operating_ratio = operating_activity_ratio(
                row["operating_activity"],
                row["net_profit"],
            )

            investing_ratio = investing_activity_ratio(
                row["investing_activity"],
                row["net_profit"],
            )

            financing_ratio = financing_activity_ratio(
                row["financing_activity"],
                row["borrowings"],
            )

            cash_margin = net_cash_flow_margin(
                row["net_cash_flow"],
                row["sales"],
            )

            cash_flag = cash_flow_flag(
                row["net_cash_flow"],
            )
            
            revenue_value = None
            revenue_flag = "INSUFFICIENT"

            pat_value = None
            pat_flag = "INSUFFICIENT"

            eps_value = None
            eps_flag = "INSUFFICIENT"

            current_year = row["year"]

            history = company_data[company_data["year"] <= current_year]

            if len(history) >= 6:

                start = history.iloc[-6]
                end = history.iloc[-1]

                revenue_value, revenue_flag = revenue_cagr(
                    start["sales"],
                    end["sales"],
                    len(history),
                    5,
                )

                pat_value, pat_flag = pat_cagr(
                    start["net_profit"],
                    end["net_profit"],
                    len(history),
                    5,
                )

                eps_value, eps_flag = eps_cagr(
                    start["eps"],
                    end["eps"],
                    len(history),
                    5,
                )
            results.append(
                {
                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "year": row["year"],
                    "broad_sector": row["broad_sector"],

                    "net_profit_margin_pct": npm,
                    "operating_profit_margin_pct": opm,
                    "opm_match": opm_match,

                    "return_on_equity_pct": roe,
                    "return_on_capital_employed_pct": roce,
                    "return_on_assets_pct": roa,

                    "debt_to_equity": de,
                    "high_leverage_flag": high_leverage,

                    "interest_coverage": icr,
                    "icr_label": label,
                    "interest_warning": warning,

                    "net_debt": nd,
                    "asset_turnover": at,
                    
                    "revenue_cagr_5yr": revenue_value,
                    "revenue_cagr_5yr_flag": revenue_flag,

                    "pat_cagr_5yr": pat_value,
                    "pat_cagr_5yr_flag": pat_flag,

                    "eps_cagr_5yr": eps_value,
                    "eps_cagr_5yr_flag": eps_flag,
                    
                    "operating_activity_ratio": operating_ratio,
                    "investing_activity_ratio": investing_ratio,
                    "financing_activity_ratio": financing_ratio,
                    "net_cash_flow_margin": cash_margin,
                    "cash_flow_flag": cash_flag,
                }
            )

    return pd.DataFrame(results)


if __name__ == "__main__":
    data = prepare_data()

    ratios = compute_financial_ratios(data)

    print(
        ratios[
            [
                "company_id",
                "year",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
                "eps_cagr_5yr",
            ]
        ].head(20)
    )

    print(f"\nTotal Records: {len(ratios)}")
