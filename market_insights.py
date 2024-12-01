import matplotlib.pyplot as plt
import streamlit as st

def market_insights_section():
    st.header("Market Insights")
    st.subheader("Stock Market Sector Performance")

    # Example data
    sectors = ["Technology", "Healthcare", "Financials", "Energy", "Utilities", "Consumer Discretionary"]
    performance = [2.5, -1.2, 1.8, -0.5, 0.7, 3.0]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(sectors, performance, color=["green" if val > 0 else "red" for val in performance])
    
    ax.set_xlabel("Sectors", fontsize=12)
    ax.set_ylabel("Performance (%)", fontsize=12)
    ax.set_title("Stock Market Sector Performance", fontsize=14)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")  # Add a baseline
    
    # Avoid setting tick labels directly; set ticks explicitly
    ax.set_xticks(range(len(sectors)))
    ax.set_xticklabels(sectors, rotation=45, ha="right", fontsize=10)

    # Add value labels to the bars for better visualization
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=10)

    st.pyplot(fig)
