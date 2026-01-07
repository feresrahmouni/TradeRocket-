import pandas as pd

def simulate_withdrawal(
    df,
    withdraw_percent,
    frequency,
    withdraw_fixed_amount=None
):
    # ---- normalize input ----
    if isinstance(df, tuple):
        df = df[0]

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    df = df.copy()
    df["Withdrawn ($)"] = 0.0

    # ---- frequency window ----
    if frequency == "monthly":
        window = 30
    elif frequency == "biweekly":
        window = 14
    elif frequency == "quarterly":
        window = 90
    else:
        window = None

    accumulated_profit = 0.0

    for i in range(len(df)):
        daily_profit = df.loc[i, "Daily Profit ($)"]
        accumulated_profit += daily_profit

        # withdrawal moment
        if window and (i + 1) % window == 0:
            if withdraw_fixed_amount is not None:
                withdraw = min(withdraw_fixed_amount, accumulated_profit)
            else:
                withdraw = accumulated_profit * withdraw_percent

            df.loc[i, "Withdrawn ($)"] = round(withdraw, 2)
            df.loc[i, "Balance ($)"] -= withdraw

            accumulated_profit = 0.0  # reset after withdrawal

    return df
