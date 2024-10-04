import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Shopylytics Solution Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.shopylytics.com',
        'About': "# This is an *extremely* cool app!",
    }
)

st.image('logo.png')
st.divider()

with st.sidebar:
    selected = option_menu(None, ["Home", "Survey Mode",  "Batch Mode",'Dashboard', 'Settings'],
        icons=['house', 'list-task', 'cloud-upload','cast', 'gear'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "lightgreen", "font-size": "25px"},
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "orange"},
        }
    )

    if selected == "Home":
        st.page_link("pages/home.py", label="Click here to continue...", icon="🏠")
    elif selected == "Survey Mode":
        st.page_link("pages/survey.py", label="Click here to continue...", icon='📈')
    elif selected == "Batch Mode":
        st.page_link("pages/batchmode.py", label="Click here to continue...", icon='📈')
    else:
        st.write("settings is my bettings")