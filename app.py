import streamlit as st
from withdrawals import simulate_withdrawal
import constants as const
from calculator import compute_growth_factor, generate_projection
from charts import display_charts
import pandas as pd


# ====== App Title ======
st.title(f"Djeja Simulator {const.EMOJI_CHICKEN}{const.EMOJI_CASH}")
st.write("---")

# ====== Inputs ======
st.subheader("Trading Inputs")

profit_percent_of_risk = st.number_input(
    "Profit per Trade (% of Risk)",
    value=float(const.DEFAULT_PROFIT_PERCENT),
    step=0.1,
    min_value=0.0
)

base_trades_per_day = st.number_input(
    "Base Trades per Day",
    value=int(const.DEFAULT_BASE_TRADES),
    step=1,
    min_value=0
)

days = st.number_input(
    "Number of Days to Project",
    value=int(const.DEFAULT_DAYS),
    step=1,
    min_value=1
)

st.write("---")

st.subheader("Bonus / Referral Trades")

extra_trades_per_day = st.number_input(
    "Extra Trades per Day",
    value=int(const.DEFAULT_EXTRA_TRADES),
    step=1,
    min_value=0
)

extra_trades_days = st.number_input(
    "Number of Days with Extra Trades",
    value=int(const.DEFAULT_EXTRA_DAYS),
    step=1,
    min_value=0
)

st.write("---")

# ====== Calculation Mode ======
mode = st.radio(
    "Calculation Mode",
    ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"]
)

# ====== Handle Starting Balance / Target Profit ======
if mode == "Target Profit ➜ Starting Balance":
    target_profit = st.number_input(
        "Target Total Profit ($)",
        value=1000.0,
        step=500.0,
        min_value=0.0
    )

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
        value=float(const.DEFAULT_STARTING_BALANCE),
        step=100.0,
        min_value=0.0
    )

# ====== Projection ======
df, final_balance = generate_projection(
    days,
    starting_balance,
    base_trades_per_day,
    extra_trades_per_day,
    extra_trades_days,
    profit_percent_of_risk
)
# ---- HARD NORMALIZATION (DO NOT REMOVE) ----
if isinstance(df, tuple):
    df = df[0]

if not isinstance(df, pd.DataFrame):
    df = pd.DataFrame(df)
# ====== Summary ======
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

# ====== Withdrawal Scenario ======
st.write("---")
st.subheader("Withdrawal Scenario")

withdraw_mode = st.radio(
    "Withdrawal Mode",
    ["Percentage of profit", "Fixed amount ($)"]
)
if withdraw_mode == "Percentage of profit":
    withdraw_percent = st.slider(
        "Withdraw % of accumulated profit",
        min_value=0,
        max_value=100,
        value=80
    ) / 100
    withdraw_fixed_amount = None
else:
    withdraw_fixed_amount = st.number_input(
        "Withdraw fixed amount ($)",
        value=1200.0,
        step=100.0,
        min_value=0.0
    )
    withdraw_percent = None


withdraw_frequency = st.selectbox(
    "Withdrawal frequency",
    ["monthly", "biweekly", "quarterly"]
)
withdraw_df = simulate_withdrawal(
    df,
    withdraw_percent,
    withdraw_frequency,
    withdraw_fixed_amount
)
# ====== Withdrawal Summary ======
st.subheader("Withdrawal Summary")
st.metric(
    "Total Profit Generated",
    f"${df['Daily Profit ($)'].sum():,.2f}"
)

st.metric(
    "Total Withdrawn",
    f"${withdraw_df['Withdrawn ($)'].sum():,.2f}"
)
# ====== Withdrawal Charts ======
st.subheader("Withdrawal Charts")

st.line_chart(
    withdraw_df.set_index("Date")["Balance ($)"]
)

st.bar_chart(
    withdraw_df.set_index("Date")["Withdrawn ($)"]
)
# ====== Withdrawal Scenario ======
if withdraw_mode == "Fixed amount ($)":
    total_profit = df["Daily Profit ($)"].sum()
    if total_profit > 0:
        implied_pct = withdraw_df["Withdrawn ($)"].sum() / total_profit * 100
        st.caption(f"≈ {implied_pct:.1f}% of total profit withdrawn")

# ===== Footer =====
st.write("---")
col1, col2 = st.columns([1, 6])

with col1:
    st.image(
        "quagmire.png",
        width=60  # very small
    )

with col2:
    st.caption("Developed by Quagmire")
     
