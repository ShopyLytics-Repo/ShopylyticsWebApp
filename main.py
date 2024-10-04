import streamlit as st
from streamlit_option_menu import option_menu
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from st_paywall import add_auth

st.set_page_config(
    page_title="Shopylytics Solution Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.shopylytics.com',
        'About': "# This is a *SaaS* based photo auditing app, developed by:orange[***SHOPYLYTICS***]!",
    }
)
with open('./config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Un-Comment below line of code to activate the SaaS Model
#add_auth(required=True)

authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.session_state["authentication_status"]:
    st.image('logo.png',output_format='auto', width=500)

    selected = option_menu(None, ["Home", "Single Mode",  "Batch Mode",'Dashboard'],
        icons=['house', 'list-task', 'cloud-upload','cast'],
        menu_icon="cast",
        default_index=0,
        orientation='horizontal',
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "lightgreen", "font-size": "25px"},
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "orange"},
        }
    )
    with st.sidebar:
        if st.session_state["name"] == 'Ato Micah':
            st.image('maverick.png',width=80)
        st.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout()
    "---"
    video_file = open('video/shopylytics_profile.mp4', 'rb')
    video_bytes = video_file.read()


    col1, col2, col3 = st.columns(3)
    with col1:
       st.write("Know about us")
       with st.container(border=True):
           st.video(video_bytes,format='video/mp4')

    with col2:
        st.write("How IRT works at SHOPYLYTICS")
        with st.container(border=True):
            st.image('Shopylytics.jpg', caption='Picturisation of Image Recognition', use_column_width=True)

    with col3:
       st.write("What next..")

    if selected == "Single Mode":
        st.switch_page("pages/singlemode.py")
    elif selected == "Batch Mode":
        st.switch_page("pages/batchmode.py")
    elif selected == "Dashboard":
        st.switch_page("pages/dashboard.py")
    st.divider()
