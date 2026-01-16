import streamlit as st 
import preprocessing , helper
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import seaborn as sns

import base64

def set_bg_image(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg_image('image.jpg')


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessing.preprocess(df,region_df)

st.sidebar.markdown("## 🏆 Olympics Analytics")
st.sidebar.markdown("Explore Olympic history with interactive data")

user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally","Overall Analysis","Country-wise Analysis")
)

st.set_page_config(
    page_title="Olympics Analytics",
    page_icon="🏅",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #161B22;
}
.main {
    background-color: #0E1117;
}
h1, h2, h3, h4 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

if user_menu == "Medal Tally":

    years , country = helper.year_country(df)

    st.sidebar.title('Medal Tally')
    selected_year = st.sidebar.selectbox("Select year",years)
    selected_country = st.sidebar.selectbox("Select country",country)

    x = helper.fetch_medal_tally(df,selected_year,selected_country)

# KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🥇 Gold", x['Gold'].sum())
    col2.metric("🥈 Silver", x['Silver'].sum())
    col3.metric("🥉 Bronze", x['Bronze'].sum())
    col4.metric("🏆 Total", x['Total'].sum())

    st.dataframe(x, use_container_width=True)

     

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]
    

    st.title("📊 Olympic Overview")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("🌍 Editions", editions)
    col2.metric("🏟 Hosts", cities)
    col3.metric("🎽 Sports", sports)
    col4.metric("🎯 Events", events)
    col5.metric("👤 Athletes", athletes)
    col6.metric("🏳 Nations", nation)


    nation_over_time = helper.participation_over_time(df)
    fig = px.line(nation_over_time, x="Edition", y="No of Countries",markers = True)
    fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
    )
    st.title('Participation over the years')
    st.plotly_chart(fig)

    events = helper.event_over_time(df)
    fig = px.line(events, x="Year", y="No of Events",markers = True)
    fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
    )
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes = helper.athlete_over_time(df)
    fig = px.line(athletes, x="Year", y="No of Athletes",markers = True)
    fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
    )
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    fig , ax = plt.subplots(figsize = (20,20))

    x= df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport',columns = 'Year',values='Event',aggfunc = 'count').fillna(0),annot = True)
    st.title('No of events over time(every sport)')
    st.pyplot(fig)


    st.title('Most successful Athletes')
    unique_sport = df['Sport'].unique().tolist()
    unique_sport.sort()
    unique_sport.insert(0,'Overall')
    


    selected_sport = st.selectbox('Select sport',unique_sport)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    unique_region = df['region'].dropna().unique().tolist()
    unique_region.sort()

    st.sidebar.title('Country-wise Analysis')
    selected_region = st.sidebar.selectbox('Select region',unique_region)

   
    country_df = helper.yearwise_medal_tally(df,selected_region)

    if country_df.empty:
        st.warning(f"🏅 **{selected_region} did not win any medals in the Olympics.**")
    else:
        st.title(f"🏅 {selected_region} – Medal Journey Over Time")
        fig = px.line(country_df, x='Year', y='Medal',markers = True)
        st.plotly_chart(fig)

        pt = helper.year_wise_sport(df,selected_region)
        fig , ax = plt.subplots(figsize = (20,20))
        ax = sns.heatmap(pt,annot = True)
        st.title(f"🔥 {selected_region} excels in these sports")
        st.pyplot(fig)

        st.title(f"🌟 Top Athletes from {selected_region}")
        x = helper.most_successful_athlete(df,selected_region)
        st.table(x)

