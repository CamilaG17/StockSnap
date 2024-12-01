import streamlit as st
from news import news_section
from market_insights import market_insights_section

def home_section():
    st.title("📈 Welcome to the Stock Dashboard")
    st.subheader("Empowering You with Smarter Stock Insights")

    st.markdown(
        """
        Unlock the power of stock market insights with our easy-to-use tools:
        - **Market Data**: Dive deep into historical stock trends and visualize them interactively.
        - **News**: Stay informed with the latest financial updates and curated news.
        - **Market Insights**: Analyze sector performance and visualize opportunities.

       
        """
    )

    # Navigation buttons
    



    # Footer with a motivational note
    st.markdown(
        """
        ---
        "Stay ahead in the market with smarter insights. Your journey begins here."
        """
    )
