import streamlit as st
from util import yt_yt as yt
from util.yt_sql import sql, YtChannelModel, YtVideosModel, YtCommentsModel
from pandas import DataFrame
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
db_name = os.environ.get('db_name')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')
db_host = os.environ.get('db_host', 'localhost')
db_port = os.environ.get('db_port', '5432')

# Initialize SQLAlchemy session
session = sql()

# Initialize YouTube API
youtube = yt.yt()

# Fetch data directly from the YouTube API or local data source
# Replace this with actual data fetching logic
channels = session.query(YtChannelModel).all()
videos = session.query(YtVideosModel).all()
comments = session.query(YtCommentsModel).all()

# Convert data to a format usable by the app
channels = [ch.__dict__ for ch in channels]
videos = [vid.__dict__ for vid in videos]
comments = [com.__dict__ for com in comments]

def reset_sql():
    session.query(YtChannelModel).delete()
    session.query(YtVideosModel).delete()
    session.query(YtCommentsModel).delete()
    session.commit()

def save(selected_channels, selected_videos, selected_comments):
    channels = [YtChannelModel(**i) for i in selected_channels]
    videos = [YtVideosModel(**i) for i in selected_videos]
    comments = [YtCommentsModel(**i) for i in selected_comments]

    session.add_all(channels)
    session.add_all(videos)
    session.add_all(comments)
    session.commit()

# Streamlit UI components
selected_ch = st.multiselect(
    label="Choose channels", 
    options=[ch['channel_name'] for ch in channels], 
)

if not selected_ch:
    st.error("Please select at least one channel.")
else:
    selected_channel_ids = [ch['channel_id'] for ch in channels if ch['channel_name'] in selected_ch]
    selected_channels = [ch for ch in channels if ch['channel_id'] in selected_channel_ids]
    selected_videos = [v for v in videos if v['channel_id'] in selected_channel_ids]
    selected_comments = [c for c in comments if c['channel_id'] in selected_channel_ids]

    st.markdown('## Selected channels data')
    st.markdown('### Channels')
    st.write(DataFrame(selected_channels))
    st.markdown('### Videos')
    st.write(DataFrame(selected_videos))
    st.markdown('### Comments')
    st.write(DataFrame(selected_comments))

    st.write('This button copies data from the selection to SQL Database')
    if st.button('Save in SQL Database'):    
        save(selected_channels, selected_videos, selected_comments)
        st.success("All entries have been saved in the tables.")

st.session_state['refresh'] = 'init'

# Show data from SQL Database
if st.session_state['refresh']:
    st.markdown('## Data in SQL Database:')
    
    # Fetch channels data
    entries = session.query(YtChannelModel).all()
    df = DataFrame([i.__dict__ for i in entries]).drop('_sa_instance_state', axis=1)
    st.markdown('### Channels')
    st.write(df)
    
    # Fetch videos data
    entries = session.query(YtVideosModel).all()
    df = DataFrame([i.__dict__ for i in entries]).drop('_sa_instance_state', axis=1)
    st.markdown('### Videos')
    st.write(df)
    
    # Fetch comments data
    entries = session.query(YtCommentsModel).all()
    df = DataFrame([i.__dict__ for i in entries]).drop('_sa_instance_state', axis=1)
    st.markdown('### Comments')
    st.write(df)

# Delete all data in SQL Database
st.write('This button deletes all entries from all tables in SQL Database')
if st.button("Delete All Entries in SQL Database"):
    reset_sql()
    st.success("All entries have been deleted from the tables.")
    st.session_state['refresh'] = 'reset'