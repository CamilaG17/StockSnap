import streamlit as st
import matplotlib.pyplot as plt

def market_insights_section():
    st.header("Market Insights")
    st.subheader("Stock Market Sector Performance")
    sectors = ["Technology", "Healthcare", "Financials", "Energy", "Utilities", "Consumer Discretionary"]
    performance = [2.5, -1.2, 1.8, -0.5, 0.7, 3.0]  # Example performance data

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sectors, performance, color=["green" if val > 0 else "red" for val in performance])
    ax.set_xlabel("Sectors")
    ax.set_ylabel("Performance (%)")
    ax.set_title("Stock Market Sector Performance")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")  # Add a baseline
    ax.set_xticklabels(sectors, rotation=45, ha="right")

    st.pyplot(fig)