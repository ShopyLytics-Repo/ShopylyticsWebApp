import os
import pandas as pd
import sys
from PIL import Image, ImageOps
import streamlit as st
from ultralytics import YOLO
import plotly.express as px
import time
from PIL import Image
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
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
    st.switch_page("main.py")
elif selected == "Batch Mode":
    st.switch_page("pages/batchmode.py")
elif selected == "Dashboard":
    st.switch_page("pages/dashboard.py")


st.header(f':blue[{surveyname}] :red[Single Mode] :orange_book:')
_LOREM_IPSUM = """
Welcome to SHOPYLYTICS's AI enabled photo auditing tool. You just need to
upload the images of your SKUs for which your model is pre-trained. Our Machine
Learning AI mode will bring the inferences our from the images.
"""

def stream_data(str_to_stream):
    for word in str_to_stream.split():
        yield word + " "
        time.sleep(0.02)

show_confidence = False

st.write_stream(stream_data(_LOREM_IPSUM))
with st.container(border=True):
    class_names = list(clsnames.values())
    allowed_classes = class_names

    st.write('Configration Panel:')
    with st.container(border=True):
        st.write('Using Custom SKUs Filter, you can further customized your results focusing the specific SKUs. By Default all SKUs that are part of your model will be included in the results.')
        custom_classes = st.checkbox('Custom SKUs Filter :ballot_box_with_check:')
        if custom_classes:
            assigned_class = st.multiselect('Select The Custom SKUs', class_names)
            if custom_classes:
                allowed_classes = assigned_class

        show_confidence = st.checkbox('Show Confidence % for detection box :ballot_box_with_check:')
        confpcnt = st.slider('Minimum Confidence % threashold',min_value=0, max_value=100, value=75, step=5)
        confpcnt = round((confpcnt/100),2)
    #st.write(f'Current Confidence % threashold is {confpcnt}')
    allowed_keylist = []
    for clsname in allowed_classes:
        for key, value in clsnames.items():
            if value == clsname:
                allowed_keylist.append(key)

    frame_window  = st.image([])
    uploaded_file = st.file_uploader("Upload Image to Detect", accept_multiple_files=False)
    if uploaded_file is not None:
        justfilename = uploaded_file.name
        img = Image.open(uploaded_file)
        img = ImageOps.exif_transpose(img)

        res = model.predict(img, task="detect", conf=confpcnt, save_crop=False, show_conf=show_confidence,classes=allowed_keylist, augment=False)[0]
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

        res = res.plot(font_size=15, line_width=1, conf=show_confidence)
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
    dfpvimg = dfpvimg.sort_values(by=['Count'], ascending=False)

    chart_data = dfpvimg

    with st.expander("Detection Summary"):
         tab1, tab2, tab3 = st.tabs(["SKUs wise share %", "SKUs wise count","Grid View"])

         with tab1:
             pie_chart = px.pie(chart_data, title='SKUs Share %', values='Count', names='Class', opacity=0.75, hole=0.5)
             st.plotly_chart(pie_chart, theme="streamlit")
             #st.write(dfpvimg.plot(kind='bar',stacked=True))

         with tab2:
             class_list = dfpvimg["Class"].values.tolist()
             count_list = dfpvimg["Count"].values.tolist()
             fig, ax = plt.subplots()
             ax.scatter(class_list[0:3], count_list[0:3])
             st.bar_chart(chart_data, x="Class", y="Count",use_container_width=True)
             st.pyplot(fig)

         with tab3:
             #st.data_editor(dfpvimg,hide_index=True,use_container_width=True)
             st.dataframe(dfpvimg,hide_index=True,use_container_width=True)
             st.info('Total number of SKUs found: '+str(int(len(dfpvimg))))

         #st.image("https://static.streamlit.io/examples/dice.jpg")

    # Every form must have a submit button.
    if st.button('Submit',key='Submitform', type="primary"):
        st.success("'Survey Data Saved Successfully!")

    if st.button('Back To Home',key='GoBackbtn'):
        st.switch_page("main.py")
