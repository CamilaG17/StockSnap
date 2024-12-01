import streamlit as st

def home_section():
    st.title("📈 Welcome to the Stock Dashboard")
    st.subheader("Empowering You with Smarter Stock Insights")

    st.markdown(
        """
        Unlock the power of stock market insights with our easy-to-use tools:
        - **Market Data**: Dive deep into historical stock trends and visualize them interactively.
        - **News**: Stay informed with the latest financial updates and curated news.
        - **Market Insights**: Analyze sector performance and visualize opportunities.

        Navigate to these features using the sidebar or the buttons below!
        """
    )

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Explore Market Data")
    with col2:
        st.button("View News")
    with col3:
        st.button("Analyze Market Insights")

    # Footer with a motivational note
    st.markdown(
        """
        ---
        "Stay ahead in the market with smarter insights. Your journey begins here."
        """
    )
