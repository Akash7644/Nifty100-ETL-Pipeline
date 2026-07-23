from typing import Optional


def operating_activity_ratio(
    operating_activity: float,
    net_profit: float,
) -> Optional[float]:

    if net_profit == 0:
        return None

    return round(operating_activity / net_profit, 2)


def investing_activity_ratio(
    investing_activity: float,
    net_profit: float,
) -> Optional[float]:

    if net_profit == 0:
        return None

    return round(investing_activity / net_profit, 2)


def financing_activity_ratio(
    financing_activity: float,
    borrowings: float,
) -> Optional[float]:

    if borrowings == 0:
        return None

    return round(financing_activity / borrowings, 2)


def net_cash_flow_margin(
    net_cash_flow: float,
    sales: float,
) -> Optional[float]:

    if sales == 0:
        return None

    return round((net_cash_flow / sales) * 100, 2)


def cash_flow_flag(
    net_cash_flow: float,
) -> str:

    if net_cash_flow < 0:
        return "NEGATIVE"

    return "POSITIVE"