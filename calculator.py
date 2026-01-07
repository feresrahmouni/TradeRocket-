from datetime import timedelta


# =========================================================
# Growth factor (used for Target Profit ➜ Starting Balance)
# =========================================================
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


# =========================================================
# Main projection used by the Streamlit app
# =========================================================
def generate_projection(
    days,
    starting_balance,
    base_trades,
    extra_trades,
    extra_days,
    profit_percent,
    start_date
):
    balance = starting_balance
    rows = []

    for day in range(1, days + 1):
        day_start_balance = balance

        trades_today = base_trades
        if day <= extra_days:
            trades_today += extra_trades

        # Apply compounding trade by trade
        for _ in range(trades_today):
            balance += balance * 0.01 * (profit_percent / 100)

        rows.append({
            "Date": start_date + timedelta(days=day - 1),
            "Day": day,
            "Trades": trades_today,
            "Daily Profit ($)": round(balance - day_start_balance, 2),
            "Balance ($)": round(balance, 2)
        })

    return rows, balance


# =========================================================
# (Optional / legacy) Simple projection function
# NOT used by the Streamlit app
# =========================================================
def calculate_projection(
    starting_balance: float,
    profit_percent_of_risk: float,
    base_trades_per_day: int,
    days: int,
    extra_trades_per_day: int = 0,
    extra_trades_days: int = 0,
    start_date=None
):
    """
    Legacy helper function.
    Not used by the Streamlit app.
    Kept only for backward compatibility.
    """

    if start_date is None:
        raise ValueError("start_date must be provided")

    balance = starting_balance
    projection = []

    for day in range(1, days + 1):
        day_start_balance = balance

        trades_today = base_trades_per_day
        if day <= extra_trades_days:
            trades_today += extra_trades_per_day

        for _ in range(trades_today):
            balance += balance * 0.01 * (profit_percent_of_risk / 100)

        projection.append({
            "Date": start_date + timedelta(days=day - 1),
            "Day": day,
            "Trades": trades_today,
            "Daily Profit ($)": round(balance - day_start_balance, 2),
            "Balance ($)": round(balance, 2)
        })

    return projection
