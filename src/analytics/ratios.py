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