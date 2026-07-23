from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Net Profit Margin = (Net Profit / Sales) × 100
    """
    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(
    operating_profit: float,
    sales: float,
    opm_percentage: Optional[float] = None,
):
    """
    Operating Profit Margin

    Returns:
        calculated_opm,
        cross_check_pass
    """

    if sales == 0:
        return None, False

    calculated = round((operating_profit / sales) * 100, 2)

    if opm_percentage is None:
        return calculated, True

    difference = abs(calculated - opm_percentage)

    return calculated, difference <= 1


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float,
) -> Optional[float]:
    """
    ROE
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float,
) -> Optional[float]:
    """
    ROCE
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(
    net_profit: float,
    total_assets: float,
) -> Optional[float]:
    """
    ROA
    """

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

def roce_benchmark(
    roce: float | None,
    broad_sector: str,
) -> bool | None:
    """
    Check whether ROCE meets the expected benchmark.

    Returns:
        True  -> Meets benchmark
        False -> Below benchmark
        None  -> ROCE could not be computed
    """

    if roce is None:
        return None

    if broad_sector == "Financials":
        # Financial institutions generally have structurally lower ROCE
        return roce >= 8

    return roce >= 15

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float,
):
    """
    Debt-to-Equity Ratio

    Returns:
        float
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)

def high_leverage_flag(
    debt_equity: float | None,
    broad_sector: str,
):
    """
    High leverage warning.

    Financial companies are excluded.
    """

    if debt_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_equity > 5

def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float,
):
    """
    Interest Coverage Ratio

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        None if interest == 0
    """

    if interest == 0:
        return None

    icr = (operating_profit + other_income) / interest

    return round(icr, 2)

def icr_label(icr):
    """
    Display label for Interest Coverage Ratio.
    """

    if icr is None:
        return "Debt Free"

    return ""

def icr_warning_flag(icr):
    """
    Interest Coverage warning.

    Returns True if company is at risk.
    """

    if icr is None:
        return False

    return icr < 1.5

def net_debt(
    borrowings: float,
    investments: float,
):
    """
    Net Debt
    """

    return round(borrowings - investments, 2)

def asset_turnover(
    sales: float,
    total_assets: float,
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)

