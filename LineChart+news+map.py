import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from decouple import config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import streamlit as st
import base64
from streamlit_navigation_bar import st_navbar

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
        passion for simplifying stock market insights. We aim to 
        empower investors and traders of all levels with real-time 
        data, intuitive tools, and actionable insights to make 
        smarter financial decisions.'''
    }
)




# Navbar styles and setup
styles = {
    "nav": {
        "background-color": "rgb(124, 215, 130)",
    }
}

page = st_navbar(
    pages=["Home", "Market Data", "News", "Market Insights"],
    styles=styles,
    options={"use_padding": False}
)

menu = st.sidebar.radio(
    "Navigate", ["Home", "Market Data", "News", "Market Insights"]
)

if page == "Home":
    new_title = '<p style="font-family:sans-serif; color: #2F4F4F; font-size: 32px;">StockSnap - Stock Market Data and Analysis App</p>'
    st.markdown(new_title, unsafe_allow_html=True)

st.markdown("""
    <style>
      div[data-testid="stHeader"] {
        z-index: 1;
      }
    </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div[data-testid="stSidebarCollapsedControl"]{
        z-index: 9999990;
        visibility: hidden;
        tabindex: -2;
      }
    	</style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        div[data-testid="stSidebarCollapseButton"] {
        visibility: hidden;    
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Commented out the logo section for testing
# with open("logo.jpg", "rb") as f:
#     data = base64.b64encode(f.read()).decode("utf-8")

#     st.sidebar.markdown(
#         f"""
#         <div style="display:table;margin-top:-30%;margin-left:10%;">
#             <img src="data:image/jpg;base64,{data}" width="200" height="50">
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# Protect API Key
apikey = config("ALPHA_API_KEY")  # Using Alpha Advantage API for stock data retrieval
news_api_key = config("NEWS_API_KEY")

symbol = st.sidebar.text_input("Enter Stock Symbol:")

# Function to fetch and process stock data
def data_frame(url, time_series_key, button):
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
        if button == 1:
            return df
        elif button == 2:
            start_date = end_date - relativedelta(months=1)
            return df[df["Timestamp"] >= start_date]
        elif button == 3:
            start_date = end_date - relativedelta(months=6)
            return df[df["Timestamp"] >= start_date]
        elif button == 4:
            start_date = end_date - relativedelta(years=1)
            return df[df["Timestamp"] >= start_date]
        elif button == 5:
            start_date = end_date - relativedelta(years=5)
            if df["Timestamp"].min() > start_date:
                st.error("Time period not available for selected symbol.")
                return None
            return df[df["Timestamp"] >= start_date]
        elif button == 6:
            start_date = end_date - relativedelta(years=10)
            if df["Timestamp"].min() > start_date:
                st.error("Time period not available for selected symbol.")
                return None
            return df[df["Timestamp"] >= start_date]
        elif button == 7:
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

    # Home Section
if menu == "Home" or page == "Home":
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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Market Data"):
            menu = "Market Data"
    with col2:
        if st.button("News"):
            menu = "News"
    with col3:
        if st.button("Market Insights"):
            menu = "Market Insights"

    # Market Data Section
elif menu == "Market Data":
    st.header("Market Data")
    with st.container():
        b1, b2, b3, b4, b5, b6, b7 = st.columns([1, 1.2, 1.2, 0.9, 1.1, 1.1, 1])
        b1_button = b1.button("Latest")
        b2_button = b2.button("1 Month")
        b3_button = b3.button("6 Months")
        b4_button = b4.button("YTD")
        b5_button = b5.button("5 Years")
        b6_button = b6.button("10 Years")
        b7_button = b7.button("All Time")
    
    if b1_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={apikey}'
        time_series_key = "Time Series (5min)"
        data = data_frame(url, time_series_key, 1)
        if data is not None:
            start_date = pd.to_datetime(data["Timestamp"].iloc[0]).strftime("for %A %B %d, %Y")
            plot_data(data, symbol, start_date)
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b2_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 2)
        if data is not None:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b3_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 3)
        if data is not None:
            end_date = datetime.now()
            start_date = end_date - relativedelta(months=6)
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b4_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 4)
        if data is not None:
            end_date = datetime.now()
            start_date = end_date - relativedelta(years=1)
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b5_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 5)
        if data is not None:
            end_date = datetime.now()
            start_date = end_date - relativedelta(years=5)
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b6_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 6)
        if data is not None:
            end_date = datetime.now()
            start_date = end_date - relativedelta(years=10)
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)
    elif b7_button:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
        time_series_key = "Monthly Time Series"
        data = data_frame(url, time_series_key, 7)
        if data is not None:
            end_date = datetime.now()
            start_date = data["Timestamp"].min()
            plot_data(data, symbol, start_date.strftime("from %B %d, %Y"), end_date.strftime("%B %d, %Y"))
            st.markdown("### Data Table")
            st.dataframe(data)

            # News Section
elif menu == "News":
    st.header("Finance News")
    news_url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&q=finance&apiKey={news_api_key}"
    response = requests.get(news_url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if articles:
            for article in articles[:5]:
                st.subheader(article.get("title", "No Title"))
                if article.get("urlToImage"):
                    st.image(article.get("urlToImage"), width=700)
                st.write(article.get("description", "No Description"))
                st.markdown(f"[Read More]({article.get('url', '#')})")
                st.markdown("---")
        else:
            st.info("No articles found.")
    else:
        st.warning("Failed to fetch news.")
        
    try:
        location_response = requests.get("https://ipinfo.io")
        if location_response.status_code == 200:
            location_data = location_response.json()
            loc = location_data.get("loc", "0,0").split(",")
            latitude, longitude = map(float, loc)
            st.write(f"Detected location: Latitude {latitude}, Longitude {longitude}")
            location_df = pd.DataFrame([{"latitude": latitude, "longitude": longitude}])
            st.map(location_df)
        else:
            st.warning("Failed to fetch location.")
    except requests.exceptions.RequestException as e:
        
        st.error(f"Error fetching location data: {e}")
        

        # Market Insights Section
elif menu == "Market Insights":
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