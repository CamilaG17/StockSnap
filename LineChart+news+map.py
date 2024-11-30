import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from decouple import config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Protect API Key
apikey = config("ALPHA_API_KEY") #Using Alpha Advantage API for stock data retrieval
news_api_key = config("NEWS_API_KEY")

symbol = st.text_input("Enter Stock Symbol:")  # Mock code to test line graph. To be replaced.

data = None


def data_frame(url, time_series_key, button):  
    if not symbol:
        st.error("Select valid stock symbol")
    else: 
        url = url 
        response = requests.get(url) # requesting data form url based on button timestamp. 

        if response.status_code == 200: #Making sure request is successful.
            st.success("Data successfully retrieved for the selected stock symbol.")
            data = response.json() # Storing .json data into variable named "data".
            time_series = data.get(time_series_key, {}) # Extracting data based on type of time series.
            df = pd.DataFrame.from_dict(time_series, orient="index") # Converting extracted data into a pandas dataframe.
            df.columns = ["Open", "High", "Low", "Close", "Volume"] #Renaming columns for simplicity.
    
            df.index = pd.to_datetime(df.index) #Turning index containing timestamps into datetime instead of string.
            df = df.sort_index()  #Sorting dataframe by the date
            df.reset_index(inplace=True) 
            df.rename(columns={"index": "Timestamp"}, inplace=True)# Renaming the index of the data "Timestamp". 
       
            end_date = datetime.now() #initializing end date variable.
            # For each button, data is filtered based on selected timeframe:
            if button == 1: 
                return df #URL for button 1 represents stock data for one stockmarket day. Timeframe does not need to be filtered.
        
            #URL for subsequent buttons represent monthly stock data from ALL TIME to most recent day the stock market was open. Timeframe needs filtering.
            elif button == 2:
                start_date = end_date - relativedelta(months=1)  #Filtering timeframe to represent one month period starting from the most recent day the stock market was open.
                df = df[df["Timestamp"] >= start_date]
                return df
            elif button ==3:
                start_date = end_date - relativedelta(months= 6) #Filtering timeframe to represent six month period starting from the most recent day the stock market was open.
                df = df[df["Timestamp"] >= start_date]
                return df
            elif button ==4:
                start_date = end_date - relativedelta(years=1) #Filtering timeframe to represent one year period starting from the most recent day the stock market was open.
                df = df[df["Timestamp"] >= start_date]
                return df
            elif button == 5:
                start_date = end_date -relativedelta(years=5) #Filtering timeframe to represent 5 year period starting from the most recent day the stock market was open.
                if df["Timestamp"].min() > start_date:
                    st.error("Time period not available for selected symbol.")  # Error if no data is available for the time period.
                    return None 
                else:
                    df = df[df["Timestamp"] >= start_date]
                    return df
            elif button ==6:
                start_date = end_date - relativedelta(years=10) #Filtering timeframe to represent 10 year period starting from the most recent day the stock market was open.
                if df["Timestamp"].min() > start_date:
                    st.error("Time period not available for selected symbol.")  # Error if no data is available for the time period.
                    return None 
                else:
                    df = df[df["Timestamp"] >= start_date]
                    return df
            elif button == 7:
                    return df
        else:
            print("Error parsing data from API") 



def plot_data(df, symbol, start_date, end_date=None): 
    title = f"{symbol} Closing Price {start_date}" #Title for plotly line graph
    if end_date:
        title += f" to {end_date}" #If end date available displaying it in the title
    
    fig = px.line(df, x="Timestamp", y="Close", title=title, labels={"Timestamp": "Timestamp", "Close": "Price"}) #Graphin plotly graph using dataframe data and setting corresponding values for axes.
    st.plotly_chart(fig, use_container_width=True) #Displaying plotly chart into Streamlit
    st.info("Use the scroll bar on the x and y-axes to view all data.")
    st.info("Hover over peaks and dips to see specific prices and timestamps.") #Instructions for users.

# Creating container to store buttons to not affect line graph placement.
with st.container():
    b1, b2, b3,b4,b5,b6,b7 = st.columns([1,1.2,1.2, 0.9,1.1, 1.1,1])  #Generating buttons and customizing button distance for evenly spaced buttons
    with b1:
        b1_button = st.button("Latest")
    with b2:
        b2_button = st.button("1 Month")
    with b3:
        b3_button = st.button("6 Months")
    with b4:
        b4_button = st.button("YTD")
    with b5:
        b5_button = st.button("5 Years")
    with b6:
        b6_button = st.button("10 Years")
    with b7:
        b7_button = st.button("All Time")

#Action when buttons clicked:
if b1_button:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={apikey}'
    time_series_key = "Time Series (5min)"
    data= data_frame(url, time_series_key, button = 1) #Calling method to extract data and create dataframe with specified parameters
    start_date =pd.to_datetime(data["Timestamp"].iloc[0]).strftime("for %A %B %d, %Y") # Converts first row of timestamp data into Weekday Name,Month, Day, and year format.
    plot_data(data, symbol, start_date) #Calling method to plot line graph with specified parameters

elif b2_button:
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url,time_series_key, button=2) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)    
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

elif b3_button:
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url, time_series_key, button=3) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=6)    
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

elif b4_button:
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url, time_series_key, button=4) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = end_date - relativedelta(years=1)
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

elif b5_button:
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url,time_series_key, button=5) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = end_date - relativedelta(years=5)    
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

elif b6_button:
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url, time_series_key, button = 6) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = end_date - relativedelta(years=10)
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

elif b7_button: 
    url =f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    time_series_key = "Monthly Time Series"
    data = data_frame(url, time_series_key, button =7) #Calling method to extract data and create dataframe with specified parameters
    end_date = datetime.now()
    start_date = data["Timestamp"].min() #Last data from dataframe
    plot_data(data, symbol, start_date=start_date.strftime("from %B %d, %Y"), end_date=end_date.strftime("%B %d, %Y")) #Calling method to plot line graph with specified parameters

    
     # Display Plot and Interactive Table
if data is not None:
    start_date = data["Timestamp"].iloc[0].strftime("%B %d, %Y")
    end_date = data["Timestamp"].iloc[-1].strftime("%B %d, %Y")
    
    
    # Stock Data Table
    st.markdown("### Stock Data Table")
    st.dataframe(data)  # Display interactive table
    
    
    
    # News Section
st.markdown("---")  # Separator
st.header("Finance News")
news_url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&q=finance&apiKey={news_api_key}"
response = requests.get(news_url)
if response.status_code == 200:
    articles = response.json().get("articles", [])
    if articles:
        for article in articles[:5]:  # Display only the first 5 articles
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            image_url = article.get("urlToImage")
            article_url = article.get("url", "#")
            
            st.subheader(title)
            if image_url:  # Display image if it exists
                st.image(image_url, width=700)
            st.write(description)
            st.markdown(f"[Read More]({article_url})")
            st.markdown("---")
    else:
        st.info("No articles found.")
else:
    st.warning("Failed to fetch news.")
# Map Section
st.markdown("---")  # Separator
st.header("Market Insights from Your Region")

# Fetch location data
try:
    location_response = requests.get("https://ipinfo.io")
    if location_response.status_code == 200:
        location_data = location_response.json()
        loc = location_data.get("loc", "0,0").split(",")
        try:
            latitude, longitude = float(loc[0]), float(loc[1])
            st.write(f"Detected location: Latitude {latitude}, Longitude {longitude}")
            # Create DataFrame for map
            location_df = pd.DataFrame([{"latitude": latitude, "longitude": longitude}])
            st.map(location_df)  # Render the map
        except ValueError as e:
            st.error(f"Failed to parse location data. Error: {e}")
    else:
        st.warning("Failed to fetch location. Check your internet connection.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching location data: {e}")