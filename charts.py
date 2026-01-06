import streamlit as st
import pandas as pd

def display_charts(projection_data):
    """
    Display charts and analytics for the projection.

    Parameters:
        projection_data: list of dicts from calculator.calculate_projection
    """

    # Convert to DataFrame
    df = pd.DataFrame(projection_data)

    st.subheader("Projection Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Analytics & Graphs")

    # 1️⃣ Balance over time
    st.line_chart(df.set_index("Date")["Balance ($)"])

    # 2️⃣ Daily Profit
    st.bar_chart(df.set_index("Date")["Daily Profit ($)"])

    # 3️⃣ Trades per day
    st.line_chart(df.set_index("Date")["Trades Today"])

    # Extra analytics
    st.subheader("Extra Analytics")
    st.write(f"- Average Daily Profit: ${df['Daily Profit ($)'].mean():.2f}")
    st.write(f"- Maximum Daily Profit: ${df['Daily Profit ($)'].max():.2f}")
    st.write(f"- Total Trades Projected: {df['Trades Today'].sum()}")
    st.write(f"- Average Trades per Day: {df['Trades Today'].mean():.2f}")
