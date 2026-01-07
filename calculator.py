from datetime import datetime, timedelta

def calculate_projection(
    starting_balance: float,
    profit_percent_of_risk: float,
    base_trades_per_day: int,
    days: int,
    extra_trades_per_day: int = 0,
    extra_trades_days: int = 0
):
    """
    Calculate daily projection of trading compounding.

    Parameters:
        starting_balance: initial capital
        profit_percent_of_risk: profit % per trade based on risk
        base_trades_per_day: regular trades per day
        days: number of days to project
        extra_trades_per_day: bonus trades per day (optional)
        extra_trades_days: number of days bonus trades are active (optional)

    Returns:
        list of dicts with each day's data: Date, Day, Trades Today, Daily Profit, Balance
    """

    balance = starting_balance
    start_date = datetime.today()
    projection = []

    for day in range(1, days + 1):
        day_start_balance = balance

        # Extra trades only for first N days
        extra_today = extra_trades_per_day if day <= extra_trades_days else 0
        trades_today = base_trades_per_day + extra_today

        # Apply compounding trade by trade
        for _ in range(trades_today):
            balance += balance * 0.01 * (profit_percent_of_risk / 100)

        daily_profit = balance - day_start_balance
        current_date = start_date + timedelta(days=day - 1)

        projection.append({
            "Date": current_date,
            "Day": day,
            "Trades Today": trades_today,
            "Daily Profit ($)": round(daily_profit, 2),
            "Balance ($)": round(balance, 2)
        })

    return projection
    
def compute_growth_factor(
    days,
    base_trades,
    extra_trades,
    extra_days,
    profit_percent
):
    factor = 1.0
    for day in range(days):
        trades_today = base_trades
        if day < extra_days:
            trades_today += extra_trades

        for _ in range(trades_today):
            factor *= (1 + 0.01 * (profit_percent / 100))
    return factor

def generate_projection(
    days,
    starting_balance,
    base_trades,
    extra_trades,
    extra_days,
    profit_percent
):
    balance = starting_balance
    rows = []

    for day in range(1, days + 1):
        day_start = balance
        trades_today = base_trades
        if day <= extra_days:
            trades_today += extra_trades

        for _ in range(trades_today):
            balance += balance * 0.01 * (profit_percent / 100)

        rows.append({
            "Day": day,
            "Trades": trades_today,
            "Daily Profit ($)": round(balance - day_start, 2),
            "Balance ($)": round(balance, 2)
        })

    return rows, balance
