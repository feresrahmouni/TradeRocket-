# app.py
import streamlit as st
import pandas as pd
import constants as const
from calculator import calculate_projection, compute_growth_factor
from charts import display_charts
from utils import count_trades_today
from datetime import datetime
import pytz

# ===== Title =====
st.title(f"Djeja Simulator {const.EMOJI_CHICKEN}{const.EMOJI_CASH}")

# Smaller image
st.image(
    "quagmire.png",
    caption="Quagmire",
    width=200
)

st.write("---")

# ===== Inputs =====
profit_percent_of_risk = st.number_input(
    "Profit per Trade (% of Risk)",
    value=const.DEFAULT_PROFIT_PERCENT,
    step=0.1
)

base_trades_per_day = st.number_input(
    "Base Trades per Day",
    value=const.DEFAULT_BASE_TRADES,
    step=1
)

days = st.number_input(
    "Number of Days",
    value=const.DEFAULT_DAYS,
    step=1
)

extra_trades_per_day = st.number_input(
    "Extra Trades per Day",
    value=const.DEFAULT_EXTRA_TRADES,
    step=1
)

extra_trades_days = st.number_input(
    "Extra Trades Duration (days)",
    value=const.DEFAULT_EXTRA_DAYS,
    step=1
)

mode = st.radio(
    "Calculation Mode",
    ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"]
)

# ===== Mode logic =====
if mode == "Target Profit ➜ Starting Balance":
    target_profit = st.number_input("Target Total Profit ($)", value=10000.0, step=500.0)
    growth_factor = compute_growth_factor(
        days,
        base_trades_per_day,
        extra_trades_per_day,
        extra_trades_days,
        profit_percent_of_risk
    )
    starting_balance = target_profit / (growth_factor - 1)
else:
    starting_balance = st.number_input(
        "Starting Balance ($)",
        value=const.DEFAULT_STARTING_BALANCE,
        step=100.0
    )

# ===== Projection =====
projection = calculate_projection(
    starting_balance,
    profit_percent_of_risk,
    base_trades_per_day,
    days,
    extra_trades_per_day,
    extra_trades_days
)

df = pd.DataFrame(projection)

# ===== Summary =====
st.subheader("Summary")
st.metric("Starting Balance", f"${starting_balance:,.2f}")
st.metric("Final Balance", f"${df.iloc[-1]['Balance ($)']:,.2f}")
st.metric(
    "Total Profit",
    f"${df.iloc[-1]['Balance ($)'] - starting_balance:,.2f}"
)

# ===== Table =====
st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

# ===== Today info =====
tz = pytz.timezone("Africa/Tunis")
now = datetime.now(tz)

today_trades = count_trades_today(
    base_trades_per_day,
    extra_trades_per_day,
    extra_trades_days,
    1
)

st.info(
    f"Current Tunis time: {now.strftime('%H:%M')} → "
    f"Trades counted today: {today_trades}"
)

# ===== Charts =====
display_charts(projection)
