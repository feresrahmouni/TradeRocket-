import streamlit as st
from calculator import calculate_projection
from charts import display_charts

# ====== App Title ======
st.title("Djeja Simulator 💰🐔")
st.write("Daily trading compounding calculator with referral extra trades.")

# ====== Inputs ======
st.subheader("Trading Parameters")
starting_balance = st.number_input("Starting Balance ($)", value=2700.0, step=100.0)
profit_percent_of_risk = st.number_input("Profit per Trade (% of Risk)", value=62.0, step=0.1)
base_trades_per_day = st.number_input("Base Trades per Day", value=2, step=1)
days = st.number_input("Number of Days to Project", value=90, step=1)

st.write("---")

st.subheader("Referral / Bonus Trades (optional)")
extra_trades_per_day = st.number_input("Extra Trades per Day", value=0, step=1)
extra_trades_days = st.number_input("Number of Days with Extra Trades", value=0, step=1)

st.write("---")

mode = st.radio("Calculation Mode", ["Starting Balance ➜ Projection", "Target Profit ➜ Starting Balance"])

# ====== Compute Projection ======
if mode == "Starting Balance ➜ Projection":
    projection = calculate_projection(
        starting_balance=starting_balance,
        profit_percent_of_risk=profit_percent_of_risk,
        base_trades_per_day=base_trades_per_day,
        days=days,
        extra_trades_per_day=extra_trades_per_day,
        extra_trades_days=extra_trades_days
    )
else:
    target_profit = st.number_input("Target Total Profit ($)", value=10000.0, step=500.0)
    # Estimate starting balance needed to reach target
    # We'll calculate projection with starting_balance=1 and scale
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
    st.write(f"Estimated starting balance needed: ${starting_balance_needed:,.2f}")
    projection = calculate_projection(
        starting_balance=starting_balance_needed,
        profit_percent_of_risk=profit_percent_of_risk,
        base_trades_per_day=base_trades_per_day,
        days=days,
        extra_trades_per_day=extra_trades_per_day,
        extra_trades_days=extra_trades_days
    )

# ====== Display Charts and Analytics ======
display_charts(projection)
