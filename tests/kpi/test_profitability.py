import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    roce_benchmark,
)


def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    value, status = operating_profit_margin(150, 1000, 15)

    assert value == 15.0
    assert status is True


def test_operating_profit_margin_mismatch():
    value, status = operating_profit_margin(100, 1000, 20)

    assert value == 10.0
    assert status is False


def test_return_on_equity():
    assert return_on_equity(100, 50, 450) == 20.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -50, 0) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(200, 100, 300, 100) == 40.0


def test_return_on_assets():
    assert return_on_assets(100, 500) == 20.0


def test_return_on_assets_zero():
    assert return_on_assets(100, 0) is None
    

def test_roce_benchmark_non_financial():
    assert roce_benchmark(18, "Industrials") is True


def test_roce_benchmark_non_financial_fail():
    assert roce_benchmark(10, "Industrials") is False


def test_roce_benchmark_financial():
    assert roce_benchmark(10, "Financials") is True


def test_roce_benchmark_none():
    assert roce_benchmark(None, "Financials") is None