import streamlit as st
from datetime import datetime
from calculator import calculate_projection
from charts import display_charts
from utils import count_trades_now
import constants as const
import pytz

# ====== App Title ======
st.title(const.APP_NAME)
st.write(const.APP_DESCRIPTION)

# ====== Inputs ======
st.subheader("Trading Parameters")
starting_balance = st.number_input(
    "Starting Balance ($)", 
    value=const.DEFAULT_STARTING_BALANCE, 
    step=100.0
)
profit_percent_of_risk = st.number_input(
    "Profit per Trade (% of Risk)", 
    value=const.DEFAULT_PROFIT_PERCENT, 
    step=0.1
)
base_trades_per_day = st.number_input(
    "Base Trades per Day", 
    value=const.DEFAULT_BASE_TRADES_PER_DAY, 
    step=1
)
days = st.number_input(
    "Number of Days to Project", 
    value=const.DEFAULT_DAYS, 
    step=1
)

st.write("---")

st.subheader("Referral / Bonus Trades (optional)")
extra_trades_per_day = st.number_input(
    "Extra Trades per Day", 
    value=const.DEFAULT_EXTRA_TRADES_PER_DAY, 
    step=1
)
extra_trades_days = st.number_input(
    "Number of Days with Extra Trades", 
    value=const.DEFAULT_EXTRA_TRADES_DAYS, 
    step=1
)

st.write("---")

mode = st.radio(
    "Calculation Mode", 
    ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"]
)

# ====== Projection ======
projection = []

if mode == "Starting Balance ➜ Projection":
    # Full projection for all days
    projection = calculate_projection(
        starting_balance=starting_balance,
        profit_percent_of_risk=profit_percent_of_risk,
        base_trades_per_day=base_trades_per_day,
        days=days,
        extra_trades_per_day=extra_trades_per_day,
        extra_trades_days=extra_trades_days
    )

else:
    # Target profit mode → estimate starting balance needed
    target_profit = st.number_input("Target Total Profit ($)", value=10000.0, step=500.0)
    projection_temp = calculate_projection(
        starting_balance=1,
        profit_percent_of_risk=profit_percent_of_risk,
        base_trades_per_day=base_trades_per_day,
        days=days,
        extra_trades_per_day=extra_trades_per_day,
        extra_trades_days=extra_trades_days
    )
    final_balance_temp = projection_temp[-1]["Balance ($)"]
    starting_balance_needed = target_profit / (final_balance_temp - 1)
    st.write(f"Estimated starting balance needed: {starting_balance_needed:,.2f}")
    projection = calculate_projection(
        starting_balance=starting_balance_needed,
        profit_percent_of_risk=profit_percent_of_risk,
        base_trades_per_day=base_trades_per_day,
        days=days,
        extra_trades_per_day=extra_trades_per_day,
        extra_trades_days=extra_trades_days
    )

# ====== Dynamic Trade Counting for Today ======
tz = pytz.timezone("Africa/Tunis")
now = datetime.now(tz)
today_dynamic_trades = count_trades_now(
    base_trades_per_day=base_trades_per_day,
    extra_trades_per_day=extra_trades_per_day,
    extra_trades_days=extra_trades_days,
    day_number=1  # today is day 1
)

st.info(
    f"Current Tunis time: {now.strftime('%H:%M')} → "
    f"Trades counted today dynamically: {today_dynamic_trades}"
)

# ====== Display Charts and Analytics ======
display_charts(projection)
