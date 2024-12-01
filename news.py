import streamlit as st
import requests
import pandas as pd

def news_section():
    st.header("Finance News")
    api_key = "f0a169fe04674c41928c65223e7ab54f"
    news_url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&q=finance&apiKey={api_key}"
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
