import os
import pandas as pd
import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageOps
import time
from streamlit_option_menu import option_menu
from datetime import datetime
import io

import ftplib
from io import StringIO
from dateutil import parser

ftp_server = "89.117.188.236"
ftp_username = "u790008942"
ftp_password = "InderRajKumar-0603"


localpath = os.getcwd()
inputfilepath = localpath + '\\Input\\'
localDbpath = localpath + '\\LocalDb\\'
outputfilepath = localpath + '\\Output\\'
modelsfilepath = localpath + '\\Models\\'

results = pd.DataFrame()
results['ImgId']       = ''
results['Class']       = ''
results['Count']       = 0
results['Probability'] = 0
results['QC Count'] = 0
results['QC Remarks'] = 0

#model = YOLO('Demo_Model_Beverage_Category.pt')
model = YOLO('MaverickC86best.pt')
clsnames = model.names
surveyname = 'In-Store Photo Audit '

st.set_page_config(
    page_title="Shopylytics Solution Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.shopylytics.com',
        'About': "# This is a *SaaS* based photo auditing app, developed by:orange[***SHOPYLYTICS***]!",
    }
)
st.image('logo.png', width=500)
selected = option_menu(None, ["Home", "Single Mode",  "Batch Mode",'Dashboard'],
    icons=['house', 'list-task', 'cloud-upload','cast'],
    menu_icon="cast",
    default_index=2,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "lightgreen", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "orange"},
    }
)

if selected == "Home":
    st.switch_page("main.py")
elif selected == "Single Mode":
    st.switch_page("pages/singlemode.py")
elif selected == "Dashboard":
    st.switch_page("pages/dashboard.py")

st.header(f':blue[{surveyname}] :red[Batch Mode] :books:')

_LOREM_IPSUM = """
Welcome to SHOPYLYTICS's AI enabled photo auditing tool. You just need to
upload the images of your SKUs for which your model is pre-trained. Our Machine
Learning AI mode will bring the inferences our from the images.
"""

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def stream_data():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)

def Check_Folder_Exist(vUploadFolderName):
    returnstatus = False
    try:
        session = ftplib.FTP(ftp_server, ftp_username, ftp_password)
        session.set_pasv(False)
        if session is not None:
            session.cwd('/domains/shopylytics.com/public_html/webapp/Maverick')
            files = []
            session.retrlines('NLST',files.append)
            for f in files:
                num=0
                if f.split()[-1] == vUploadFolderName:
                    returnstatus = True
                    exit
    except ftplib.all_errors as e:
            print(f'FTP error:{e}')
    return returnstatus

def showupload(placeholder):
    df = pd.DataFrame(columns=['filename', 'fileType', 'modifydate'])
    session = ftplib.FTP(ftp_server, ftp_username, ftp_password)
    session.set_pasv(False)
    session.cwd('/domains/shopylytics.com/public_html/webapp/Maverick')
    for name, data in list(session.mlsd()):
        if data.get("type").upper().strip() not in('CDIR','PDIR'):
            row = {'filename': name.strip(), 'fileType': data.get("type").upper().strip(),'modifydate': parser.parse((data.get('modify').strip()))}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
    df.sort_values(by=['modifydate'], ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    placeholder.dataframe(df,
                 column_config={
                     "filename": st.column_config.TextColumn(
                         "Name",
                     ),
                     "fileType": st.column_config.TextColumn(
                         "Type",
                     ),
                     "modifydate": st.column_config.DatetimeColumn(
                         "Upload DateTime",
                         format="D MMM YYYY, h:mm a",
                         step=60,
                     ),

                 },
                 hide_index=True, width=800
                 )


st.write_stream(stream_data)
placeholder1 = st.empty()
placeholder2 = st.empty()

with st.expander("Create New Upload:"):
    startdatetime = datetime.now()
    enddatetime = datetime.now()
    time_diff = enddatetime - startdatetime
    UploadFolder = 'upload_' + startdatetime.strftime("%d_%m_%Y_%Hh_%Mm_%Ss")
    UploadFolderName = st.text_input('Upload Name', UploadFolder)
    uploaded_file = st.file_uploader("Upload a Image File", accept_multiple_files=True)
    if ((uploaded_file is not None) & (len(uploaded_file) > 0)):
        try:

            session = ftplib.FTP(ftp_server, ftp_username, ftp_password)
            session.set_pasv(False)
            session.cwd('/domains/shopylytics.com/public_html/webapp/Maverick')
            try:
                if Check_Folder_Exist(UploadFolderName):
                    session.cwd(f'/domains/shopylytics.com/public_html/webapp/Maverick/{UploadFolderName}')
                else:
                    session.mkd(UploadFolderName)
                    session.cwd(f'/domains/shopylytics.com/public_html/webapp/Maverick/{UploadFolderName}')
                    print(f'dirctory {UploadFolderName} created successully. Uploading the files now!')
            except ftplib.all_errors as e:
                print('FTP error:', e)

            filecount = len(uploaded_file)
            for i in range(len(uploaded_file)):
                upload_filename = uploaded_file[i]
                if upload_filename.name.endswith('jpg'):
                    session.storbinary("STOR " + upload_filename.name, upload_filename)
                    upload_filename.close()
            session.quit()
            st.success(f"Total {filecount} files uploaded successfully under {UploadFolderName} Folder to the FTP server: {ftp_server}!")
            placeholder1.info('List of file and folder you had already uploaded (In Descending Order):')
            showupload(placeholder2)
        except ftplib.all_errors as e:
            print('FTP error:', e)

placeholder1.info('List of file and folder you had already uploaded (In Descending Order):')
showupload(placeholder2)

if st.button('Back To Home',key='GoBackbtn'):
    st.switch_page("main.py")
