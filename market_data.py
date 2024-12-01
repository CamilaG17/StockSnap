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
        elif button == 4:  # Last 1 Year
            start_date = end_date - relativedelta(years=1)
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
        elif button == 7:  # Custom Range
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

# Market data section
def market_data_section():
    st.header("Market Data")

    # Sidebar inputs
    symbol = st.text_input("Enter Stock Symbol:")
    api_key = "AFX49MY5XQM0TTH7"  # Replace with a valid API key
    time_series_key = "Time Series (Daily)"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    # Buttons for data range selection
    button = st.radio(
        "Select Time Range",
        (
            "All Data",
            "Last 1 Month",
            "Last 6 Months",
            "Last 1 Year",
            "Last 5 Years",
            "Last 10 Years",
            "Custom Range",
        ),
        index=0,
    )

    # Map button text to numeric values
    button_map = {
        "All Data": 1,
        "Last 1 Month": 2,
        "Last 6 Months": 3,
        "Last 1 Year": 4,
        "Last 5 Years": 5,
        "Last 10 Years": 6,
        "Custom Range": 7,
    }

    selected_button = button_map[button]

    # Fetch and filter data
    df = data_frame(url, time_series_key, selected_button, symbol)

    # Plot data if available
    if df is not None:
        start_date = df["Timestamp"].min().strftime("%Y-%m-%d")
        end_date = df["Timestamp"].max().strftime("%Y-%m-%d") if selected_button != 1 else None
        plot_data(df, symbol, start_date, end_date)
