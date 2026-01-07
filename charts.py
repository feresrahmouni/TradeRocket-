import streamlit as st
import pandas as pd

def display_charts(df: pd.DataFrame):
    """
    Display charts and analytics for the projection.
    Expects a DataFrame with columns:
    - El bonus arjaa ghodwa (day)
    - Trades
    - Daily Profit ($)
    - Balance ($)
    """

    st.subheader("Analytics & Graphs")

    # ===== Balance over time =====
    if "Balance ($)" in df.columns:
        st.line_chart(df["Balance ($)"])
    else:
        st.warning("Balance data not found")

    # ===== Daily profit =====
    if "Daily Profit ($)" in df.columns:
        st.bar_chart(df["Daily Profit ($)"])
    else:
        st.warning("Daily profit data not found")

    # ===== Trades per day =====
    if "Trades" in df.columns:
        st.line_chart(df["Trades"])
    else:
        st.warning("Trades data not found")

    # ===== Extra analytics =====
    st.subheader("Extra Analytics")

    if "Daily Profit ($)" in df.columns:
        st.write(f"- Average Daily Profit: ${df['Daily Profit ($)'].mean():.2f}")
        st.write(f"- Maximum Daily Profit: ${df['Daily Profit ($)'].max():.2f}")

    if "Trades" in df.columns:
        st.write(f"- Total Trades Projected: {int(df['Trades'].sum())}")
        st.write(f"- Average Trades per Day: {df['Trades'].mean():.2f}")
