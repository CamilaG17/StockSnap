import streamlit as st
import base64
from streamlit_navigation_bar import st_navbar
import requests
from home import home_section
from market_data import market_data_section
from news import news_section
from market_insights import market_insights_section

# Custom Navigation Bar
styles = {
    "nav": {
        "background-color": "rgb(124, 215, 130)",
    }
}

# Placeholder for custom navbar function (or replace with your implementation)
page = st_navbar(
    pages=["StockSnap", ""],
    styles=styles,
    options={"use_padding": False}
)

if page == "StockSnap":
    new_title = '<p style="font-family:sans-serif; color: #2F4F4F; font-size: 32px;">StockSnap - Stock Market Data and Analysis App</p>'
    st.markdown(new_title, unsafe_allow_html=True)


# Logo handling for the sidebar
with open("logo.jpg", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

    st.sidebar.markdown(
        f"""
        <div style="display:table;margin-top:-30%;margin-left:10%;">
            <img src="data:image/jpg;base64,{data}" width="200" height="50">
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        z-index: 20;
        top: 0%; 
        height: 100% !important;
        background-color: #FFFFFF;
      }
    </style>""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar.title (" "):
    menu = st.sidebar.radio(
    label="Navigate", options=
    ["Home", "Market Data", "News", "Market Insights"]
)

# Dynamic content rendering based on navigation
if menu == "Home":
    home_section()
elif menu == "Market Data":
    market_data_section()
elif menu == "News":
    news_section()
elif menu == "Market Insights":
    market_insights_section()

# Additional Custom Styles
st.markdown("""
    <style>
        div[data-testid="stHeader"] {
            z-index: 1;
        }
        div[data-testid="stSidebarCollapsedControl"] {
            z-index: 9999990;
            visibility: hidden;
        }
        div[data-testid="stSidebarCollapseButton"] {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)
