import streamlit as st
import matplotlib.pyplot as plt
from pandas import DataFrame
from psycopg2 import Binary
from sqlalchemy import create_engine, text
from util import yt_yt as yt
from util.yt_df import df_with_link

# PostgreSQL connection setup
DATABASE_URL = "postgresql://username:password@localhost:5432/db_name"
engine = create_engine(DATABASE_URL)

youtube = yt.yt()
chIds = []

# Function to update entries from the PostgreSQL database
def updateEntries():
    global chIds
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM channels"))
        dfChannels = DataFrame(result.fetchall(), columns=result.keys())
        st.session_state['dfChannels'] = dfChannels
        if st.session_state['dfChannels'].shape[0] > 0:
            chIds = dfChannels['channel_id'].tolist()
updateEntries()

def make_clickable(url):
    return f'<a target="_blank" href="{url}">{url}</a>'

def plot(df):
    st.markdown('### Performance of latest 50 videos')
    st.line_chart(df[['view_count', 'like_count', 'comment_count']])

def scrape():
    chId = st.text_input('Channel ID')
    if chId in chIds: 
        st.error('Channel data already exists. Give different channel ID')
    st.write('On clicking the below button the data related to this channel ID is requested from Youtube Data API.')
    if st.button('Get Details') and chId and chId not in chIds:
        chDetails = youtube.getChDetails(chId)
        if chDetails == -1:
            st.error("Can't get channel details. Check channel ID.")
        else:
            # Get data from YouTube API
            videos = youtube.getVideos(chDetails['videos_id'])
            ytComments = [] 
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            for j in range(len(videos)):
                i = videos[j]
                res = youtube.getComments(i['video_id'])
                ytComments.extend(res)
                progress_bar.progress((j+1)*2)
                status_text.text(f'{(j+1)*2} % Complete')
            progress_bar.empty()
            status_text.text('Scraping completed')

            # Displaying
            st.markdown('### Latest videos')
            dfVids = DataFrame(videos)

            dfVids['url'] = 'https://www.youtube.com/watch?v=' + dfVids['video_id']
            df_with_link(dfVids, 'title', 'url')

            plot(dfVids)

            catNames = youtube.getCategories()
            fig, ax = plt.subplots()
            slice_sizes = (dfVids['category_id'].value_counts() / dfVids.shape[0]) * 100
            slice_sizes = slice_sizes.reset_index()
            labels = [catNames[i] for i in slice_sizes['category_id']]
            ax.pie(slice_sizes['count'], labels=labels, startangle=90)
            ax.axis('equal')
            st.markdown('### Content category:')
            st.pyplot(fig)

            # Saving in PostgreSQL
            with engine.connect() as connection:
                connection.execute(
                    text("INSERT INTO channels (channel_id, channel_name, subscriber_count, video_count) VALUES (:channel_id, :channel_name, :subscriber_count, :video_count)"),
                    {
                        "channel_id": chDetails['channel_id'],
                        "channel_name": chDetails['channel_name'],
                        "subscriber_count": chDetails['subscriber_count'],
                        "video_count": chDetails['video_count']
                    }
                )
                connection.execute(
                    text("INSERT INTO videos (video_id, channel_id, title, view_count, like_count, comment_count, category_id) VALUES (:video_id, :channel_id, :title, :view_count, :like_count, :comment_count, :category_id)"),
                    [
                        {
                            "video_id": video['video_id'],
                            "channel_id": chDetails['channel_id'],
                            "title": video['title'],
                            "view_count": video['view_count'],
                            "like_count": video['like_count'],
                            "comment_count": video['comment_count'],
                            "category_id": video['category_id']
                        }
                        for video in videos
                    ]
                )
                connection.execute(
                    text("INSERT INTO comments (video_id, comment_text) VALUES (:video_id, :comment_text)"),
                    [
                        {
                            "video_id": comment['video_id'],
                            "comment_text": comment['comment_text']
                        }
                        for comment in ytComments
                    ]
                )

            # Update entries
            updateEntries()         

st.write("# Scrape Youtube Channels Data")

scrape()

if st.session_state['dfChannels'].shape[0] > 0:
    st.markdown('### Channels in PostgreSQL:')
    st.write(st.session_state['dfChannels'])

if st.session_state['dfChannels'].shape[0] > 0 and st.button('Delete all data in PostgreSQL'):
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM comments"))
        connection.execute(text("DELETE FROM videos"))
        connection.execute(text("DELETE FROM channels"))

    st.session_state['dfChannels'] = None
    st.rerun()