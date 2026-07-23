from src.analytics.cashflow_kpis import (
    operating_activity_ratio,
    investing_activity_ratio,
    financing_activity_ratio,
    net_cash_flow_margin,
    cash_flow_flag,
)


def test_operating_activity_ratio():
    assert operating_activity_ratio(200, 100) == 2.0


def test_operating_activity_zero_profit():
    assert operating_activity_ratio(200, 0) is None


def test_investing_activity_ratio():
    assert investing_activity_ratio(-50, 100) == -0.5


def test_financing_activity_ratio():
    assert financing_activity_ratio(100, 200) == 0.5


def test_financing_zero_borrowings():
    assert financing_activity_ratio(100, 0) is None


def test_net_cash_flow_margin():
    assert net_cash_flow_margin(100, 1000) == 10.0


def test_cash_flow_flag_positive():
    assert cash_flow_flag(50) == "POSITIVE"


def test_cash_flow_flag_negative():
    assert cash_flow_flag(-10) == "NEGATIVE"