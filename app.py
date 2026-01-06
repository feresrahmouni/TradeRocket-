import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ====== App Title ======
st.title("Djeja Simulator 🐔")
st.write("Daily trading compounding calculator with referral extra trades.")

# ====== Inputs ======
starting_balance = st.number_input("Starting Balance ($)", value=2700.0, step=100.0)
profit_percent_of_risk = st.number_input("Profit per Trade (% of Risk)", value=62.0, step=0.1)
base_trades_per_day = st.number_input("Base Trades per Day", value=2, step=1)
days = st.number_input("Number of Days to Project", value=90, step=1)

st.write("---")

# ====== Extra Trades ======
st.subheader("Referral / Bonus Trades (optional)")
extra_trades_per_day = st.number_input("Extra Trades per Day", value=0, step=1)
extra_trades_days = st.number_input("Number of Days with Extra Trades", value=0, step=1)

st.write("---")

# ====== Core Calculation ======
balance = starting_balance
start_date = datetime.today()
rows = []

for day in range(1, int(days) + 1):
    day_start_balance = balance

    # Extra trades only for first N days
    extra_today = extra_trades_per_day if day <= extra_trades_days else 0
    trades_today = base_trades_per_day + extra_today

    # Apply compounding trade by trade
    for _ in range(trades_today):
        balance += balance * 0.01 * (profit_percent_of_risk / 100)

    daily_profit = balance - day_start_balance
    current_date = start_date + timedelta(days=day - 1)

    rows.append({
        "Date": current_date,
        "Day": day,
        "Trades Today": trades_today,
        "Daily Profit ($)": round(daily_profit, 2),
        "Balance ($)": round(balance, 2)
    })

df = pd.DataFrame(rows)

# ====== Display Table ======
st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

# ====== Summary ======
st.subheader("Summary")
st.metric("Starting Balance", f"${starting_balance:,.2f}")
st.metric("Final Balance", f"${balance:,.2f}")
st.metric("Total Profit", f"${balance - starting_balance:,.2f}")

# ====== Analytics & Charts ======
st.subheader("Analytics & Graphs")

# Balance over time
st.line_chart(df.set_index("Date")["Balance ($)"])

# Daily profit
st.bar_chart(df.set_index("Date")["Daily Profit ($)"])

# Trades per day
st.line_chart(df.set_index("Date")["Trades Today"])

# Extra analytics
st.subheader("Extra Analytics")
st.write(f"- Average Daily Profit: ${df['Daily Profit ($)'].mean():.2f}")
st.write(f"- Maximum Daily Profit: ${df['Daily Profit ($)'].max():.2f}")
st.write(f"- Total Trades Projected: {df['Trades Today'].sum()}")
st.write(f"- Average Trades per Day: {df['Trades Today'].mean():.2f}")
