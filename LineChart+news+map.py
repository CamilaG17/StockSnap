import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from decouple import config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from home import home_section
from news import news_section
from market_insights import market_insights_section
import base64

# Protect API Keys
apikey = config("ALPHA_API_KEY")  # Alpha Vantage API Key
news_api_key = config("NEWS_API_KEY")  # News API Key

if "menu" not in st.session_state:
    st.session_state.menu = "Home"

# Set up page configuration
st.set_page_config(
    page_title="StockSnap",
    page_icon=":chart:",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://docs.streamlit.io/",
        "Report a bug": None,
        "About": '''Our app was developed by a team of five dedicated students 
        from **Florida International University**, driven by a shared 
        passion for simplifying stock market insights.'''
    }
)

# Sidebar Navigation
menu = st.sidebar.radio("Navigate", ["Home", "Market Data", "News", "Market Insights"])

if menu != st.session_state.menu:
    st.session_state.menu = menu

with open("logo-Photoroom.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

    st.sidebar.markdown(
        f"""
        <div style="display:table;margin-top:-72%;margin-left:10%;">
            <img src="data:image/jpg;base64,{data}" width="200" height="50">
        </div>
        """,
        unsafe_allow_html=True,
    )
   
def data_frame(url, time_series_key, button):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get(time_series_key, {})
        if not time_series:
            st.error("No data found for the selected symbol.")
            return None
        
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Timestamp"}, inplace=True)
        return df
    else:
        st.error("Error retrieving data from the API.")
        return None

# Function to plot stock data
def plot_data(df, symbol, start_date, end_date=None):
    title = f"{symbol} Closing Price {start_date}"
    if end_date:
        title += f" to {end_date}"
    fig = px.line(
        df, x="Timestamp", y="Close", 
        title=title, labels={"Timestamp": "Timestamp", "Close": "Price"}
    )
    st.plotly_chart(fig, use_container_width=True)
    


# Home Section
if st.session_state.menu == "Home":
    home_section()
    

# Market Data Section
if st.session_state.menu == "Market Data":
    st.header("Market Data")
    symbol = st.text_input("Enter Stock Symbol (ex. AAPL):").strip()

    if not symbol:
        st.warning("Please enter a valid stock symbol.")
    else:
        
        with st.container():
            b1, b2, b3, b4, b5, b6, b7 = st.columns([1, 1.2, 1.2, 0.9, 1.1, 1.1, 1])
            b1_button = b1.button("Latest")
            b2_button = b2.button("1 Month")
            b3_button = b3.button("6 Months")
            b4_button = b4.button("YTD")
            b5_button = b5.button("5 Years")
            b6_button = b6.button("10 Years")
            b7_button = b7.button("All Time")

        # Handle button actions
        if b1_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={apikey}"
            time_series_key = "Time Series (5min)"
            data = data_frame(url, time_series_key, 1)
            if data is not None:
                start_date = pd.to_datetime(data["Timestamp"].iloc[0]).strftime("for %A %B %d, %Y")
                plot_data(data, symbol, start_date)
                st.dataframe(data)

        elif b2_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}"
            time_series_key = "Time Series (Daily)"
            data = data_frame(url, time_series_key, 2)
            if data is not None:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.dataframe(data)

        elif b3_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}"
            time_series_key = "Time Series (Daily)"
            data = data_frame(url, time_series_key, 3)
            if data is not None:
                end_date = datetime.now()
                start_date = end_date - relativedelta(months=6)
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.dataframe(data)
        elif b4_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={"AFX49MY5XQM0TTH7"}'
            time_series_key = "Monthly Time Series"
            data = data_frame(url, time_series_key, 4)
            if data is not None:
                end_date = datetime.now()
                start_date = end_date - relativedelta(years=1)
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.markdown("### Data Table")
                st.dataframe(data)
        elif b5_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={"AFX49MY5XQM0TTH7"}'
            time_series_key = "Monthly Time Series"
            data = data_frame(url, time_series_key, 5)
            if data is not None:
                end_date = datetime.now()
                start_date = end_date - relativedelta(years=5)
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.markdown("### Data Table")
                st.dataframe(data)
        elif b6_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={"AFX49MY5XQM0TTH7"}'
            time_series_key = "Monthly Time Series"
            data = data_frame(url, time_series_key, 6)
            if data is not None:
                end_date = datetime.now()
                start_date = end_date - relativedelta(years=10)
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.markdown("### Data Table")
                st.dataframe(data)
        elif b7_button:
            st.success(f"Data for {symbol} retrieved successfully")
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={"AFX49MY5XQM0TTH7"}'
            time_series_key = "Monthly Time Series"
            data = data_frame(url, time_series_key, 7)
            if data is not None:
                end_date = datetime.now()
                start_date = data["Timestamp"].min()
                plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
                st.markdown("### Data Table")
                st.dataframe(data)

   

# News Section
if st.session_state.menu == "News":
    news_section()

# Market Insights Section
if st.session_state.menu == "Market Insights":
    market_insights_section()


st.markdown(
    """
    <style>
        div[data-testid="stSidebarCollapsedControl"] {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
