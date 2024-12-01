import streamlit as st
import base64
from home import home_section
from market_data import market_data_section
from news import news_section
from market_insights import market_insights_section
from streamlit_navigation_bar import st_navbar

# Set page configuration
st.set_page_config(
    page_title="StockSnap",
    page_icon=":chart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': '''Our app was developed by a team of five dedicated students 
        from **Florida International University**, driven by a shared 
        passion for simplifying stock market insights. We aim to 
        empower investors and traders of all levels with real-time 
        data, intuitive tools, and actionable insights to make 
        smarter financial decisions.'''
    }
)
# Custom Navigation Bar
styles = {
    "nav": {
        "background-color": "rgb(124, 215, 130)",
    }
}

page = st_navbar(
    pages=["StockSnap", ""],
    styles=styles,
    options={"use_padding": False}
)
if page == "StockSnap":
    new_title = '<p style="font-family:sans-serif; color: #2F4F4F; font-size: 32px;">StockSnap - Stock Market Data and Analysis App</p>'
    st.markdown(new_title, unsafe_allow_html=True)
# Logo handling for the sidebar
with open("logo.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")
    st.sidebar.markdown(
        f"""
        <div style="display:table;margin-top:-10%;margin-left:10%;text-align:center;">
            <img src="data:image/jpg;base64,{data}" width="200" height="50">
        </div>
        """,
        unsafe_allow_html=True,
    )

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

# Initialize session state for menu
if "menu" not in st.session_state:
    st.session_state["menu"] = "Home"

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    label="Navigate to:",
    options=["Home", "Market Data", "News", "Market Insights"],
    index=["Home", "Market Data", "News", "Market Insights"].index(st.session_state.get("menu", "Home"))
)

# Update session state if the radio button is clicked
if st.session_state.get("menu") != menu:
    st.session_state["menu"] = menu  # Set session state, rerun happens automatically

# Render the appropriate section
if st.session_state["menu"] == "Home":
    home_section()
elif st.session_state["menu"] == "Market Data":
    market_data_section()
elif st.session_state["menu"] == "News":
    news_section()
elif st.session_state["menu"] == "Market Insights":
    market_insights_section()

# Footer
st.sidebar.markdown(
    """
    ---
    **StockSnap App**  
    Created with 💡 and ☕ by [Your Name].
    """
)
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        z-index: 20;
      }
    </style>""", unsafe_allow_html=True)

