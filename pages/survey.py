import os
import pandas as pd
import sqlite3
import sys
from PIL import Image
import streamlit as st
from ultralytics import YOLO
import plotly.express as px
from pathlib import Path
import numpy as np
import torch
import time
import cv2
import requests
from PIL import Image
from streamlit_option_menu import option_menu
#from cv2 import *

#from datetime import time

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

localpath = os.getcwd()
inputfilepath = localpath + '\\Input\\'
localDbpath = localpath + '\\LocalDb\\'
outputfilepath = localpath + '\\Output\\'
modelsfilepath = localpath + '\\Models\\'

localdbname= 'Shopylytics.db'

conn = sqlite3.connect(localdbname, timeout=20)
df_Survay = pd.read_sql_query("select * from Survay;", conn)
#print(df_Survay.head())

clslst = [
"dog","person","cat","tv","car","meatballs","marinara sauce","tomato soup","chicken noodle soup","french onion soup",
"chicken breast","ribs","pulled pork","hamburger","cavity","Tata Tea Gold Window","Tata Tea Gold","Tata Sampann Chilli Powder",
"Tata Sampann Window","Tata Sampann Turmeric Powder","Tata Sampann Coriander Powder","MamyPoko Extra Absorb Pants",
"MamyPoko Pants Standard Pant","Pampers Premium Care Pants","Pampers All round Protection Pants",
"Mothercare Quick Absorb Diaper Pants","Pampers New Baby Taped Diapers","Pampers Active Baby Diapers",
"Tata Chakra Gold","Tata Chakra Gold Elaichi","Tata Tea Gold Care","Tata Tetley Green Tea","Tata Tetley Green Lemon & Honey Tea",
"Tata Tea Premium","Brooke Bond Taj Mahal Tea","Brooke Bond Red Label","Brooke Bond Red Label Natural Care Tea",
"Brooke Bond Red Label Tea","Tata Agni Tea","Tata Tea Elaichi Chai","Tata Agni Strong Tea","Tata Agni Adrak Tea",
"Tata Tea Agni Elaichi","Brook Bond 3 Roses","Wagh Bakri Premium Spiced Tea","SOCIETY TEA Masala","Girnar Royal Cup Tea",
"Society Tea","Ganesh Premium Tea","Brook Bond Taaza","Tata Tea Kanan Devan Strong","Tata Tea Kanan Devan Clasisic",
"Tata Tea Gold Darjeeling","Wagh Bakri Premium Leaf Tea","Wagh Bakri Good Morning Premium Tea","Wagh Bakri Gold",
"Wagh Bakri Mili Premium","Wagh Bakri Navchetan Leaf Tea","Tata Tea Kanan Devan Golden Leaf","Girnar Detox Green Tea",
"Girnar Green Tea Cardamom","Brooke Bond Taaza Tea Masala Chaska","Tata Tea Gold Saffron","Lipton Green Tea",
"Girnar Masala Chai","Girnar Cardamom Chai","Tata Coffee Specials Hazelnut","Nestle Gold Cappuccino","Bru Green Label Coffee",
"Bru Instant Coffee","Tata Tea Premium Teaveda","Tea Valley Classic Tea","Tea Valley Royal","Lipton Yellow Label Tea",
"Nestea Lemon Ice Tea","Marvel Red Tea","Marvel Masala Tea","Girnar Green Tea Mint","Girnar Green Tea Lemon",
"Girnar Green Tea Lemon & Honny","Society Premium Green Tea","Society Shake To Make Mango","Wagh Bakri Instant Masala Tea",
"Wagh Bakri Instant Elaichi","AVT Premium Tea","Everest Masala Tea","Tata Tetley Lemon","Wagh Bakri Instant Ginger Tea",
"Macha Tea Classic","Macha Tea Classic Tulsi Adrak Elaichi","Organic India Classic Tulsi Green Tea",
"Organic India Tulsi Detox Kahwa Green Tea","Organic India Tulsi Sweet Rose","Organic India Tulsi Ginger Turmeric Green Tea",
"Society Pure Assam Dust Tea","Nescafe Classic Instant Coffee","Nescafe Classic Black Roast Coffee",
"Nescafe Sunrise Instant Coffee","Organic India Tulsi Honey Chamomile Tea","Organic India Tulsi Masala Chai","Dabur Vedic Tea",
"Tata Coffee Gold","Nescafe Gold Blend Instant Coffee","Tata Coffee Grand Pouch","Tata Coffee Grand",
"Tetley Black Tea Lemon Twist","Tetley Black Tea Masala Chai","Bru Gold Aromatic Instant Coffee","Bru Super Strong Instant Coffee",
"Nescafe Gold Cappuccino","Nescafe Gold Choco Mocha","Tata Coffee Grand Filter Coffee","AVT Premium Coffee",
"Lipton Darjeeling Long Leaf Tea","Tata Lal Ghora Tea","Girnar Variety Pack Chai","Girnar Ginger Chai","Girnar Express Chai",
"Girnar Stevia Chai","Girnar 3 in 1 Coffee","Girnar Kashmiri Kahwa","Girnar Lemon Tea","Girnar Calming Green Tea",
"Girnar Haldi Doodh","Girnar Safron Chai","Tata Tea Premium Kadak Assam Tea","Tata Tetley Elichi Tea","Nescafe 3 in 1 Coffee",
"Tata Tetley Masala Tea","Tata Tetley Ginger Zing","Tata Tetley Ginger","Tata Tetley Ginger Tea","Tata Tetley Original","Tea Valley Gold"]



## Now fatching the list of organization from history table
#df_orgname.loc[:, 'organisation'] = df_orgname['organisation'].str.upper()
#df_orgname.loc[:, 'organisation'] = df_orgname['organisation'].str.strip()
#org_list = df_orgname.organisation.values.tolist()
conn.close()

results = pd.DataFrame()
results['ImgId']       = ''
results['Class']       = ''
results['Count']       = 0
results['Probability'] = 0
results['QC Count'] = 0
results['QC Remarks'] = 0

model = YOLO('Demo_Model_Beverage_Category.pt')

surveyname = 'In-Store Photo Audit '

st.set_page_config(
    page_title="Shopylytics Solution Hub",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.shopylytics.com',
        'About': "# This is an *extremely* cool app!",
    }
)
st.image('logo.png')
st.divider()
selected = option_menu(None, ["Home", "Survey Mode",  "Batch Mode",'Dashboard', 'Settings'],
    icons=['house', 'list-task', 'cloud-upload','cast', 'gear'],
    menu_icon="cast",
    default_index=1,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "lightgreen", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "orange"},
    }
)

if selected == "Home":
    st.switch_page("pages/home.py")
elif selected == "Batch Mode":
    st.switch_page("pages/batchmode.py")
else:
    st.write("settings is my bettings")

st.header(f':blue[{surveyname}] :red[Survey Mode] :clipboard:')



with st.container(border=True):
    surveyoption = st.selectbox(
    'Please select the survey you wish to start',
    ('TCPL CI','Gopalji DB Survey'))
    st.write('You selected:', surveyoption)

    #st.dataframe(df_Survay)

    for ind in df_Survay.index:
        lv_Question_Text   = df_Survay['Question_Text'][ind]
        lv_Question_Type   = df_Survay['Question_Type'][ind]
        lv_Control_Key     = df_Survay['Control_Key'][ind]
        lv_Control_Visible = df_Survay['Control_Visible'][ind]

        if lv_Question_Type == "Yes_No":
            genre = st.radio(lv_Question_Text,["Yes", "No"],horizontal=True)

        if lv_Question_Type == "Text":
            lv_Control_Key = st.text_input(lv_Question_Text, lv_Question_Text)
            st.write(f'For Question {lv_Question_Text} You answered: ', lv_Control_Key)

        if lv_Question_Type == "Numeric":
            lv_number_Key = st.number_input(lv_Question_Text)
            st.write(f'For Question {lv_Question_Text} You answered: ', lv_number_Key)


    frame_window  = st.image([])
    uploaded_file = st.file_uploader("Upload Category Area Image", accept_multiple_files=False)
    if uploaded_file is not None:
        bytes_data    = uploaded_file.read()
        imgNp = np.array(bytearray(bytes_data), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, cv2.IMREAD_UNCHANGED)

        res = model.predict(frame, task="detect", conf=0.75, save_crop=False, show_conf=True, augment=False)[0]
        rowid = 0
        for box in res.boxes:
            class_id = res.names[box.cls[0].item()]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            conf = round(box.conf[0].item(), 2)
            results.loc[rowid, 'ImgId'] = uploaded_file.name
            results.loc[rowid, 'Class'] = class_id
            results.loc[rowid, 'Probability'] = conf
            results.loc[rowid, 'Count'] = 1
            results.loc[rowid, 'QC Count'] = 1
            results.loc[rowid, 'QC Remarks'] = conf
            # results.loc[rowid, 'cords'] = cords
            rowid += 1

        res = res.plot(font_size=15, line_width=1, conf=True)
        res = res[:, :, ::-1]
        res = Image.fromarray(res)
        frame_window.image(res)


    #st.balloons()
    # img_file_buffer = st.camera_input("Close shot of category area",key='closeshotimg')
    # if img_file_buffer:
    #     #bytes_data = img_file_buffer.getvalue()
    #     #torch_img = torch.ops.image.decode_image(
    #     #    torch.from_numpy(np.frombuffer(bytes_data, np.uint8)), 3 )
    #     image = Image.open(img_file_buffer)
    #     image.thumbnail((640, 640))
    #
    #     res = model.predict(image, task="detect", conf=0.75, save_crop=False, show_conf=True, augment=False)[0]
    #     rowid = 0
    #     for box in res.boxes:
    #         class_id = res.names[box.cls[0].item()]
    #         cords = box.xyxy[0].tolist()
    #         cords = [round(x) for x in cords]
    #         conf = round(box.conf[0].item(), 2)
    #
    #         results.loc[rowid, 'ImgId'] = 'Close Shot of Category'
    #         results.loc[rowid, 'Class'] = class_id
    #         results.loc[rowid, 'Probability'] = conf
    #         results.loc[rowid, 'Count'] = 1
    #         results.loc[rowid, 'QC Count'] = 1
    #         results.loc[rowid, 'QC Remarks'] = conf
    #         # results.loc[rowid, 'cords'] = cords
    #         rowid += 1
    #
    #     res = res.plot(font_size=15, line_width=1, conf=True)
    #     res = res[:, :, ::-1]
    #     res = Image.fromarray(res)
    #     st.image(res)

    dfpvtable = pd.pivot_table(results, values='Count', index=['ImgId'], columns=['Class'],aggfunc='count').reset_index()
    dfpvtable.fillna(0, inplace=True)
    dfimg = results[:][['ImgId','Class', 'Count']]
    #dfimg = results[:][['Class', 'Count']]
    dfpvimg  = dfimg.groupby(['ImgId','Class'])['Count'].sum().reset_index()
    #dfpvimg = dfimg.groupby(['Class'])['Count'].sum().reset_index()
    dfpvimg['Count'] = dfpvimg['Count'].astype(int)

    chart_data = dfpvimg

    with st.expander("Detection Summary"):
         tab1, tab2, tab3 = st.tabs(["SKUs wise share %", "SKUs wise count","Grid View"])

         with tab1:
             pie_chart = px.pie(chart_data, title='SKUs Share %', values='Count', names='Class', opacity=0.75, hole=0.5)
             st.plotly_chart(pie_chart, theme="streamlit")

         with tab2:
             st.bar_chart(chart_data, x="Class", y="Count",use_container_width=True)

         with tab3:
             st.dataframe(dfpvimg,hide_index=True,use_container_width=True)
             st.info('Total number of SKUs found: '+str(int(len(dfpvimg))))

         #st.image("https://static.streamlit.io/examples/dice.jpg")

    # Every form must have a submit button.
    if st.button('Submit',key='Submitform', type="primary"):
        st.success("'Survey Data Saved Successfully!")

    if st.button('End Survey',key='GoBackbtn'):
        st.switch_page("pages/home.py")
