import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import plotly.express as px


# Function to fetch and process stock data
def data_frame(url, time_series_key, button, symbol):
    if not symbol:
        st.error("Select a valid stock symbol.")
        return None
    response = requests.get(url)
    if response.status_code == 200:
        st.success("Data successfully retrieved for the selected stock symbol.")
        data = response.json()
        time_series = data.get(time_series_key, {})
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Timestamp"}, inplace=True)

        end_date = datetime.now()
        if button == 1:  # All Data
            return df
        elif button == 2:  # Last 1 Month
            start_date = end_date - relativedelta(months=1)
            return df[df["Timestamp"] >= start_date]
        elif button == 3:  # Last 6 Months
            start_date = end_date - relativedelta(months=6)
            return df[df["Timestamp"] >= start_date]
        elif button == 4:  # YTD (Year to Date)
            start_date = datetime(end_date.year, 1, 1)
            return df[df["Timestamp"] >= start_date]
        elif button == 5:  # Last 5 Years
            start_date = end_date - relativedelta(years=5)
            if df["Timestamp"].min() > start_date:
                st.error("Time period not available for selected symbol.")
                return None
            return df[df["Timestamp"] >= start_date]
        elif button == 6:  # Last 10 Years
            start_date = end_date - relativedelta(years=10)
            if df["Timestamp"].min() > start_date:
                st.error("Time period not available for selected symbol.")
                return None
            return df[df["Timestamp"] >= start_date]
        elif button == 7:  # All Time
            return df
    else:
        st.error("Error parsing data from API.")
        return None

# Function to plot stock data
def plot_data(df, symbol, start_date, end_date=None):
    title = f"{symbol} Closing Price {start_date}"
    if end_date:
        title += f" to {end_date}"
    fig = px.line(df, x="Timestamp", y="Close", title=title, labels={"Timestamp": "Timestamp", "Close": "Price"})
    st.plotly_chart(fig, use_container_width=True)
    st.info("Use the scroll bar on the x and y-axes to view all data.")
    st.info("Hover over peaks and dips to see specific prices and timestamps.")

# # Market Data Section
def market_data_section():
    st.header("📊 Market Data")
    st.write("Search for stocks and visualize their historical data interactively.")


    # Sidebar: stock symbol input
    symbol = st.text_input("Enter Stock Symbol:")
    api_key = "AFX49MY5XQM0TTH7"  # Replace with a valid API key
    time_series_key = "Time Series (Daily)"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    # Search bar at the top and buttons for data range selection
    st.subheader("Select Time Range")

    with st.container():
        b1, b2, b3, b4, b5, b6, b7 = st.columns([1, 1.2, 1.2, 0.9, 1.1, 1.1, 1])
        b1_button = b1.button("Latest")
        b2_button = b2.button("1 Month")
        b3_button = b3.button("6 Months")
        b4_button = b4.button("YTD")
        b5_button = b5.button("5 Years")
        b6_button = b6.button("10 Years")
        b7_button = b7.button("All Time")

       # Fetch and filter data
    if symbol and not any([b1_button, b2_button, b3_button, b4_button, b5_button, b6_button, b7_button]):
        # Automatically set the default button to "Latest" if no button is pressed
        selected_button = 1  # Default to "Latest"
    elif any([b1_button, b2_button, b3_button, b4_button, b5_button, b6_button, b7_button]):
        # Map the pressed button to its respective range
        if b1_button:
            selected_button = 1  # Latest
        elif b2_button:
            selected_button = 2  # 1 Month
        elif b3_button:
            selected_button = 3  # 6 Months
        elif b4_button:
            selected_button = 4  # YTD
        elif b5_button:
            selected_button = 5  # 5 Years
        elif b6_button:
            selected_button = 6  # 10 Years
        elif b7_button:
            selected_button = 7  # All Time
    else:
        selected_button = None

    # Fetch and filter data
    if selected_button:
        df = data_frame(url, time_series_key, selected_button, symbol)

        # Plot data if available
        if df is not None:
            start_date = df["Timestamp"].min().strftime("%Y-%m-%d")
            end_date = df["Timestamp"].max().strftime("%Y-%m-%d") if selected_button != 1 else None
            plot_data(df, symbol, start_date, end_date)


