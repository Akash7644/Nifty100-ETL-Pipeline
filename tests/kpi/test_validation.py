from pathlib import Path
import pandas as pd


def test_validation_report_exists():
    assert Path("reports/validation_summary.csv").exists()


def test_log_file_exists():
    assert Path("logs/ratio_edge_cases.log").exists()


def test_validation_report_not_empty():
    df = pd.read_csv("reports/validation_summary.csv")
    assert not df.empty


def test_validation_columns():
    df = pd.read_csv("reports/validation_summary.csv")

    expected_columns = [
        "Total Rows",
        "Missing ROE",
        "Missing ROA",
        "Missing Debt to Equity",
        "Missing Revenue CAGR",
        "Negative Cash Flow",
    ]

    for column in expected_columns:
        assert column in df.columns