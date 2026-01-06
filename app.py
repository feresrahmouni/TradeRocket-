import streamlit as st
from datetime import datetime, timedelta

# ====== App Title ======
st.title("TradeCompound 🚀")
st.write("Daily trading compounding calculator with referral extra trades.")

# ====== Inputs ======
starting_balance = st.number_input("Starting Balance ($)", value=2700, step=100)
risk_percent = st.number_input("Risk per Trade (%)", value=1.0, step=0.1)
profit_percent_of_risk = st.number_input("Profit per Trade (% of Risk)", value=62.0, step=0.1)
trades_per_day = st.number_input("Base Trades per Day", value=2, step=1)
days = st.number_input("Number of Days to Project", value=90, step=1)

st.write("---")

# ====== Referral / Extra Trades Input ======
st.write("Referral / Extra Trades (optional): Add extra trades for N consecutive days.")
extra_trades_events = []

if st.checkbox("Add Extra Trades Event"):
    start_day = st.number_input("Start Day", value=1, step=1)
    extra_trades = st.number_input("Extra Trades", value=1, step=1)
    duration_days = st.number_input("Duration (days)", value=4, step=1)
    if st.button("Add Event"):
        extra_trades_events.append((start_day, extra_trades, duration_days))
        st.success(f"Added: {extra_trades} extra trades from day {start_day} for {duration_days} days")

# ====== Core Calculation ======
balance = starting_balance
start_date = datetime.today()

# Table header
st.write("Date | Day | Balance | Daily Profit | Trades Today")
st.write("---")

for day in range(1, int(days)+1):
    day_start_balance = balance

    # Check extra trades active today
    extra_trades_today = 0
    for event in extra_trades_events:
        start, extra, duration = event
        if start <= day < start + duration:
            extra_trades_today += extra

    today_trades = trades_per_day + extra_trades_today

    # Apply compounding per trade
    for trade in range(today_trades):
        balance += balance * (risk_percent / 100) * (profit_percent_of_risk / 100)

    daily_profit = balance - day_start_balance
    current_date = start_date + timedelta(days=day-1)

    st.write(f"{current_date.strftime('%Y-%m-%d')} | {day} | {balance:.2f} | {daily_profit:.2f} | {today_trades}")
