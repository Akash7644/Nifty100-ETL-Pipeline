from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
)


def test_debt_to_equity():
    assert debt_to_equity(200, 100, 300) == 0.5


def test_debt_free():
    assert debt_to_equity(0, 100, 300) == 0


def test_negative_equity():
    assert debt_to_equity(100, -50, 0) is None


def test_high_leverage_true():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_false():
    assert high_leverage_flag(2, "Industrials") is False


def test_financial_company():
    assert high_leverage_flag(20, "Financials") is False
    
from src.analytics.ratios import (
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)


def test_interest_coverage():
    assert interest_coverage_ratio(300, 50, 50) == 7.0


def test_interest_zero():
    assert interest_coverage_ratio(300, 50, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2) is True


def test_icr_safe():
    assert icr_warning_flag(4.5) is False


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero():
    assert asset_turnover(1000, 0) is None