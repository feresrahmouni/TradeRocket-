import streamlit as st
import pandas as pd

def display_charts(data):
    """
    Accepts either:
    - pandas DataFrame
    - OR list of dicts
    """

    # ---- Normalize input to DataFrame ----
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.DataFrame(data)

    if df.empty:
        st.warning("No data to display")
        return

    st.subheader("Analytics & Graphs")

    # ===== Balance over time =====
    if "Balance ($)" in df.columns:
        st.line_chart(df["Balance ($)"])
    else:
        st.warning("Missing column: Balance ($)")

    # ===== Daily Profit =====
    if "Daily Profit ($)" in df.columns:
        st.bar_chart(df["Daily Profit ($)"])
    else:
        st.warning("Missing column: Daily Profit ($)")

    # ===== Trades per day =====
    if "Trades" in df.columns:
        st.line_chart(df["Trades"])
    else:
        st.warning("Missing column: Trades")

    # ===== Extra analytics =====
    st.subheader("Extra Analytics")

    if "Daily Profit ($)" in df.columns:
        st.write(f"- Average Daily Profit: ${df['Daily Profit ($)'].mean():.2f}")
        st.write(f"- Maximum Daily Profit: ${df['Daily Profit ($)'].max():.2f}")

    if "Trades" in df.columns:
        st.write(f"- Total Trades Projected: {int(df['Trades'].sum())}")
        st.write(f"- Average Trades per Day: {df['Trades'].mean():.2f}")
