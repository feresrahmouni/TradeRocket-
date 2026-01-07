import pandas as pd

def simulate_withdrawal(df, withdraw_percent, frequency):
    # 🔒 HARD NORMALIZATION (DO NOT REMOVE)
    if isinstance(df, tuple):
        df = df[0]

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    df = df.copy()
    df["Withdrawn ($)"] = 0.0

    for i in range(len(df)):
        profit = df.loc[i, "Daily Profit ($)"]
        withdraw = profit * withdraw_percent

        if frequency == "biweekly" and i % 14 != 0:
            withdraw = 0
        elif frequency == "quarterly" and i % 90 != 0:
            withdraw = 0

        df.loc[i, "Withdrawn ($)"] = withdraw
        df.loc[i, "Balance ($)"] -= withdraw

    return df
