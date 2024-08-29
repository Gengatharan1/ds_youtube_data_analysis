import streamlit as st
import pandas as pd
import altair as alt
from util import yt_yt as yt
from util.yt_sql import sql, YtChannelModel, YtVideosModel, YtCommentsModel
from util.yt_df import df_with_link
from sqlalchemy import func

# Initialize SQLAlchemy session
session = sql()

# Load YouTube utility
youtube = yt.yt()

# Get category mappings
categories = {value: key for key, value in youtube.getCategories().items()}

st.markdown("# Analyse SQL Data")

st.markdown("### Views of the last 50 videos")

def create_chart(df):
    chart = alt.Chart(df).mark_line().encode(
        x='published:T',
        y='view_count:Q',
        color='channel_name:N',
        tooltip=['published:T', 'view_count:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()
    return chart

# Fetch data from PostgreSQL
channels = pd.DataFrame(session.query(YtChannelModel.channel_id, YtChannelModel.channel_name).all(), columns=['channel_id', 'channel_name'])
videos_query = session.query(
    YtVideosModel.title, 
    YtVideosModel.video_id, 
    YtVideosModel.channel_id, 
    YtVideosModel.view_count, 
    YtVideosModel.published, 
    YtVideosModel.category_id
).order_by(YtVideosModel.published.desc()).limit(50)

videos = pd.DataFrame(videos_query.all(), columns=['title', 'video_id', 'channel_id', 'view_count', 'published', 'category_id'])

# Add channel name to videos dataframe
videos['channel_name'] = videos['channel_id'].map(channels.set_index('channel_id')['channel_name'])
st.altair_chart(create_chart(videos), use_container_width=True)

st.markdown("### Filter category of videos in each channel")

# Create category select box
selected_option = st.selectbox(
    'Select a category:',
    categories.keys()
)
category_id = categories[selected_option]

# Display the selected category
st.write('Category:', selected_option)

# Filter videos by selected category
df_categories = videos[videos['category_id'] == category_id]

if df_categories.empty:
    st.warning('No videos available for this category')
else:
    df_count = df_categories.groupby('channel_name').size().reset_index(name='Video Count').sort_values('Video Count', ascending=False)
    st.write('Sorted by video count in descending order')
    st.write(df_count)

    for channel_name in df_count['channel_name']:
        with st.expander(channel_name):
            df_vids = df_categories[df_categories['channel_name'] == channel_name][['title', 'video_id']]
            df_vids['video_id'] = 'https://www.youtube.com/watch?v=' + df_vids['video_id']
            df_vids = df_vids.rename(columns={'title': 'Videos'}).reset_index(drop=True)
            df_with_link(df_vids, 'Videos', 'video_id')