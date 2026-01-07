import streamlit as st
from constants import *
from calculator import compute_growth_factor, generate_projection
from charts import display_charts

# ====== App Title & Image ======
st.title(f"Djeja Simulator {EMOJI_CHICKEN}{EMOJI_CASH}")
st.image(
    "assets/quagmire.png",  # put the image in your repo /assets folder
    caption=f"Quagmire {EMOJI_QUAGMIRE}",
    use_column_width=True
)
st.write("---")

# ====== Inputs ======
st.subheader("Trading Inputs")
profit_percent_of_risk = st.number_input(
    "Profit per Trade (% of Risk)", value=DEFAULT_PROFIT_PERCENT, step=0.1
)
base_trades_per_day = st.number_input(
    "Base Trades per Day", value=DEFAULT_BASE_TRADES, step=1
)
days = st.number_input("Number of Days to Project", value=DEFAULT_DAYS, step=1)

st.write("---")

st.subheader("Bonus / Referral Trades")
extra_trades_per_day = st.number_input(
    "Extra Trades per Day", value=DEFAULT_EXTRA_TRADES, step=1
)
extra_trades_days = st.number_input(
    "Number of Days with Extra Trades", value=DEFAULT_EXTRA_DAYS, step=1
)

st.write("---")

# ====== Calculation Mode ======
mode = st.radio("Calculation Mode", ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"])

# ====== Handle Starting Balance / Target Profit ======
if mode == "Target Profit ➜ Starting Balance":
    target_profit = st.number_input("Target Total Profit ($)", value=1000.0, step=500.0)
    growth_factor = compute_growth_factor(
        days, base_trades_per_day, extra_trades_per_day, extra_trades_days, profit_percent_of_risk
    )
    starting_balance = target_profit / (growth_factor - 1)
else:
    starting_balance = st.number_input(
        "Starting Balance ($)", value=DEFAULT_STARTING_BALANCE, step=100.0
    )

# ====== Projection ======
df, final_balance = generate_projection(
    days, starting_balance, base_trades_per_day, extra_trades_per_day, extra_trades_days, profit_percent_of_risk
)

# ====== Summary (Top) ======
st.subheader("Summary")
st.metric("Starting Balance", f"${starting_balance:,.2f}")
st.metric("Final Balance", f"${final_balance:,.2f}")
st.metric("Total Profit", f"${final_balance - starting_balance:,.2f}")

st.write("---")

# ====== Projection Table ======
st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

# ====== Analytics & Charts ======
display_charts(df)

st.info("Current Tunis time → Trades today counted dynamically based on thresholds")
