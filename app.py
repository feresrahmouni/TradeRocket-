import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import pytz

# ===== Timezone =====
tz = pytz.timezone("Africa/Tunis")
now = datetime.now(tz)

# ===== App Title =====
st.title("Djeja Simulator 💰🐔")

# ===== Inputs =====
profit_percent_of_risk = st.number_input("Profit per Trade (% of Risk)", value=62.0, step=0.1)
base_trades_per_day = st.number_input("Base Trades per Day", value=2, step=1)
days = st.number_input("Number of Days", value=90, step=1)
extra_trades_per_day = st.number_input("Extra Trades per Day", value=0, step=1)
extra_trades_days = st.number_input("Extra Trades Duration (days)", value=0, step=1)
mode = st.radio("Calculation Mode", ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"])

st.write("---")

# ===== Define trade time thresholds (Tunis time) =====
trade_thresholds = [time(13, 39), time(18, 39)]  # Base trades
bonus_thresholds = [time(18, 49), time(18, 59)]  # Bonus trades

# ===== Function to count trades today based on time =====
def count_trades_today(day):
    trades = 0
    # Base trades
    for t in trade_thresholds[:base_trades_per_day]:
        if now.time() >= t:
            trades += 1
    # Bonus trades (only for first extra_trades_days)
    if day <= extra_trades_days:
        for t in bonus_thresholds[:extra_trades_per_day]:
            if now.time() >= t:
                trades += 1
    return trades

# ===== Growth Factor Calculation =====
def compute_growth_factor():
    factor = 1.0
    for day in range(1, days + 1):
        trades_today = count_trades_today(day)
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
    trades_today = count_trades_today(day)
    for _ in range(trades_today):
        balance += balance * 0.01 * (profit_percent_of_risk / 100)
    daily_profit = balance - day_start

    rows.append({
        "Date": start_date + timedelta(days=day - 1),
        "Day": day,
        "Trades": trades_today,
        "Daily Profit": round(daily_profit, 2),
        "Balance": round(balance, 2)
    })

df = pd.DataFrame(rows)

# ===== Display Table =====
st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

# ===== Summary =====
st.subheader("Summary")
st.metric("Starting Balance", f"${starting_balance:,.2f}")
st.metric("Final Balance", f"${balance:,.2f}")
st.metric("Total Profit", f"${balance - starting_balance:,.2f}")

st.info(f"Current Tunis time: {now.strftime('%H:%M')} → Trades today counted dynamically based on thresholds")

# ===== Analytics & Graphs using Streamlit native charts =====
st.subheader("Analytics & Graphs")

# 1️⃣ Balance Over Time
st.line_chart(df.set_index("Date")["Balance"])

# 2️⃣ Daily Profit
st.bar_chart(df.set_index("Date")["Daily Profit"])

# 3️⃣ Trades per Day
st.line_chart(df.set_index("Date")["Trades"])

# ===== Extra Analytics =====
st.subheader("Extra Analytics")
st.write(f"- Average Daily Profit: ${df['Daily Profit'].mean():.2f}")
st.write(f"- Maximum Daily Profit: ${df['Daily Profit'].max():.2f}")
st.write(f"- Total Trades Projected: {df['Trades'].sum()}")
st.write(f"- Average Trades per Day: {df['Trades'].mean():.2f}")
