import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# ===== Timezone =====
tz = pytz.timezone("Europe/Brussels")
now = datetime.now(tz)

# ===== App Title =====
st.title("TradeCompound 💰🐔")

# ===== Inputs =====
profit_percent_of_risk = st.number_input("Profit per Trade (% of Risk)", value=62.0, step=0.1)
base_trades_per_day = st.number_input("Base Trades per Day", value=2, step=1)
days = st.number_input("Number of Days", value=90, step=1)

st.write("---")

extra_trades_per_day = st.number_input("Extra Trades per Day", value=0, step=1)
extra_trades_days = st.number_input("Extra Trades Duration (days)", value=0, step=1)

st.write("---")

mode = st.radio("Calculation Mode", ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"])

# ===== Time Logic =====
bonus_starts_today = now.hour < 20
bonus_offset = 1 if bonus_starts_today else 2

st.info(
    f"Current Belgium time: {now.strftime('%H:%M')} → "
    f"Bonus starts on day {bonus_offset}"
)

# ===== Growth Factor Calculation =====
def compute_growth_factor():
    factor = 1.0
    for day in range(1, days + 1):
        extra_today = extra_trades_per_day if bonus_offset <= day < bonus_offset + extra_trades_days else 0
        trades_today = base_trades_per_day + extra_today
        for _ in range(trades_today):
            factor *= (1 + 0.01 * (profit_percent_of_risk / 100))
    return factor

growth_factor = compute_growth_factor()

# ===== Mode Handling =====
if mode == "Starting Balance ➜ Projection":
    starting_balance = st.number_input("Starting Balance ($)", value=2700.0, step=100.0)
else:
    target_profit = st.number_input("Target Total Profit ($)", value=10000.0, step=500.0)
    starting_balance = target_profit / (growth_factor - 1)

# ===== Projection =====
balance = starting_balance
rows = []
start_date = now.date()

for day in range(1, days + 1):
    day_start = balance
    extra_today = extra_trades_per_day if bonus_offset <= day < bonus_offset + extra_trades_days else 0
    trades_today = base_trades_per_day + extra_today

    for _ in range(trades_today):
        balance += balance * 0.01 * (profit_percent_of_risk / 100)

    rows.append({
        "Date": (start_date + timedelta(days=day - 1)).isoformat(),
        "Day": day,
        "Trades": trades_today,
        "Daily Profit ($)": round(balance - day_start, 2),
        "Balance ($)": round(balance, 2)
    })

df = pd.DataFrame(rows)

# ===== Display =====
st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

st.subheader("Summary")
st.metric("Starting Balance", f"${starting_balance:,.2f}")
st.metric("Final Balance", f"${balance:,.2f}")
st.metric("Total Profit", f"${balance - starting_balance:,.2f}")
