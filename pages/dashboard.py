import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import requests
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu


warnings.filterwarnings('ignore')

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
    default_index=3,
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
elif selected == "Batch Mode":
    st.switch_page("pages/batchmode.py")

surveyname = 'In-Store Photo Audit '
st.header(f':blue[{surveyname}] :red[Dashboard] :books:')



st.title(" :bar_chart: Self-Care Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
#if fl is not None:
#    filename = fl.name
#   st.write(filename)
#   df = pd.read_csv(filename, encoding="ISO-8859-1")
#else:
url = "https://github.com/arunmathur27/PowerBIDatabase/raw/main/DetailsResults.xlsx"
myfile = requests.get(url)
df = pd.read_excel(myfile.content, sheet_name='DetailsResults', engine='openpyxl')

    #url = "https://github.com/arunmathur27/PowerBIDatabase/raw/main/SKU_Brand.xlsx"
    #myfile = requests.get(url)
    #SKU_Brand = pd.read_excel(myfile.content, engine='openpyxl')
    #os.chdir(r"C:\Users\Arun Mathur\PycharmProjects\St_dashboard")
    #df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")



#df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date
#startDate = pd.to_datetime(df["Order Date"]).min()
#endDate = pd.to_datetime(df["Order Date"]).max()

st.write(df)
#fig = ff.create_table(df, colorscale="Earth")
#st.plotly_chart(fig, use_container_width=True)

st.sidebar.header("Choose your filter: ")
# Create for Region
region = st.sidebar.multiselect("Pick the Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]
#
# Create for State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]
#

# Create for City
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())
if not city:
    df4 = df3.copy()
else:
    df4 = df3[df3["City"].isin(city)]

#
# # Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]
#
category_df = filtered_df.groupby(by=["Class"], as_index=False)["Count"].sum()
#
col1, col2 = st.columns(2)
with col1:
    st.subheader("Class wise Count")
    fig = px.bar(category_df, x="Class", y="Count", text=['${:,.2f}'.format(x) for x in category_df["Count"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)
#
with col2:
    st.subheader("Region wise Count")
    fig = px.pie(filtered_df, values="Count", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
#
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Class_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Class.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by="Region", as_index=False)["Count"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
#
# filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
# st.subheader('Time Series Analysis')
#
linechart = pd.DataFrame(
    filtered_df.groupby(filtered_df["Class"])["Count"].sum()).reset_index()
fig2 = px.line(linechart, x="Class", y="Count", labels={"Class": "Class"}, height=500, width=1000,
               template="gridon")
st.plotly_chart(fig2, use_container_width=True)
#
# with st.expander("View Data of TimeSeries:"):
#     st.write(linechart.T.style.background_gradient(cmap="Blues"))
#     csv = linechart.to_csv(index=False).encode("utf-8")
#     st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')
#
# Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Count using TreeMap")
fig3 = px.treemap(filtered_df, path=["Region", "State", "City"], values="Count", hover_data=["Count"],
                  color="City")
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)

"---"
st.subheader('Region wise Counts')
fig = px.pie(filtered_df, values="Count", names="Region", template="gridon")
fig.update_traces(text=filtered_df["Region"], textposition="inside")
st.plotly_chart(fig, use_container_width=True)

R1cols1, R1cols2 = st.columns(2)

with R1cols1:
    st.subheader('State wise Counts')
    fig = px.pie(filtered_df, values="Count", names="State", template="gridon")
    fig.update_traces(text=filtered_df["State"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
    #
with R1cols2:
    st.subheader('City wise Counts')
    fig = px.pie(filtered_df, values="Count", names="City", template="gridon")
    fig.update_traces(text=filtered_df["City"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


R2cols1, R2cols2 = st.columns(2)
with R2cols1:
    st.subheader('Brand wise Count')
    fig = px.pie(filtered_df, values="Count", names="Brand", template="plotly_dark")
    fig.update_traces(text=filtered_df["Brand"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with R2cols2:
    st.subheader('Class wise Sales')
    fig = px.pie(filtered_df, values="Count", names="Class", template="gridon")
    fig.update_traces(text=filtered_df["Class"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
#
#
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region", "State", "City", "Class", "Brand", "Count"]]
    fig = ff.create_table(df_sample, colorscale="Earth")
    st.plotly_chart(fig, use_container_width=True)

# # Create a scatter plot
data1 = px.scatter(filtered_df, x="Brand", y="Class", size="Count")
data1['layout'].update(title="Relationship between Brand and Counts using Scatter Plot.",
                       titlefont=dict(size=20), xaxis=dict(title="Brand Wise Count", titlefont=dict(size=19)),
                       yaxis=dict(title="Class Wise Count", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)
#
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500, 0:20:1].style.background_gradient(cmap="Oranges"))
#
# Download orginal DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

if st.button('Back To Home', key='GoBackbtn'):
    st.switch_page("main.py")
