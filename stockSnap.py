import streamlit as st
import base64
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title="StockSnap",
    page_icon=":chart:",
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

# navbar starts here
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

st.markdown("""
    <style>
      div[data-testid="stHeader"] {
        z-index: 1;tockS
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
# navbar ends here


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

with st.sidebar.title(" "):
    tab = st.sidebar.radio(label=" ",options=["Home","Market Data","News","Market Analysis"])
if tab == "Home":
    st.subheader("Homepage is displayed here")
elif tab == "Market Data":
    st.subheader("Market Data is displayed here")
elif tab == "News":
    st.subheader("News page is displayed here")
else:
    st.subheader("Market Analysis is displayed here")

st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        z-index: 20;
        top: 5%; 
        height: 95% !important;
        background-color: #FFFFFF;
      }
    </style>""", unsafe_allow_html=True)
