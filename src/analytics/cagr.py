from typing import Optional


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int,
):
    """
    CAGR Formula

    Returns:
        (cagr_value, flag)
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), "NORMAL"

def has_sufficient_history(total_years, required_years):
    return total_years >= required_years

def revenue_cagr(
    start_sales,
    end_sales,
    total_years,
    period,
):
    if not has_sufficient_history(total_years, period):
        return None, "INSUFFICIENT"

    return calculate_cagr(
        start_sales,
        end_sales,
        period,
    )
    
def pat_cagr(
    start_profit,
    end_profit,
    total_years,
    period,
):
    if not has_sufficient_history(total_years, period):
        return None, "INSUFFICIENT"

    return calculate_cagr(
        start_profit,
        end_profit,
        period,
    )

def eps_cagr(
    start_eps,
    end_eps,
    total_years,
    period,
):
    if not has_sufficient_history(total_years, period):
        return None, "INSUFFICIENT"

    return calculate_cagr(
        start_eps,
        end_eps,
        period,
    )

