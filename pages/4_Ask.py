import streamlit as st
from sqlalchemy import func
from pandas import DataFrame, Timedelta
from util.yt_sql import sql, YtChannelModel as ch, YtVideosModel as v, YtCommentsModel as cm
from util.yt_df import df_with_link

# Initialize SQLAlchemy session
session = sql()

st.markdown('## Get answers for questions:')

# Query 1: Names of all videos and their corresponding channels
with st.expander("1 - What are the names of all the videos and their corresponding channels?"):
    result = session.query(
        v.title.label('Video Name'), 
        ch.channel_name.label('Channel Name'),
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).join(ch, v.channel_id == ch.channel_id).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')

# Query 2: Channels with the most number of videos
with st.expander("2 - Which channels have the most number of videos, and how many videos do they have?"):
    result = session.query(
        ch.channel_name, ch.thumbnail, ch.vid_count
    ).order_by(ch.vid_count.desc()).first()

    st.write(f"{result.channel_name} channel has the most number of videos: {result.vid_count}")
    # st.image(result.thumbnail)

# Query 3: Top 10 most viewed videos and their respective channels
with st.expander("3 - What are the top 10 most viewed videos and their respective channels?"):
    result = session.query(
        v.title.label('Video Name'), 
        v.view_count.label('Views'), 
        ch.channel_name.label('Channel Name'),
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).join(ch, v.channel_id == ch.channel_id).order_by(v.view_count.desc()).limit(10).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')

# Query 4: Number of comments on each video and their corresponding video names
with st.expander("4 - How many comments were made on each video, and what are their corresponding video names?"):
    result = session.query(
        v.title.label('Video Name'), 
        v.comment_count.label('Comments'),
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')

# Query 5: Videos with the highest number of likes and their corresponding channel names
with st.expander("5 - Which videos have the highest number of likes, and what are their corresponding channel names?"):
    result = session.query(
        v.title.label('Video Name'), 
        v.like_count.label('Likes'), 
        ch.channel_name.label('Channel Name'),
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).join(ch, v.channel_id == ch.channel_id).order_by(v.like_count.desc()).limit(10).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')

# Query 6: Total number of likes for each video and their corresponding video names
with st.expander("6 - What is the total number of likes and dislikes for each video, and what are their corresponding video names?"):
    result = session.query(
        v.title.label('Video Name'), 
        v.like_count.label('Likes'),
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')

# Query 7: Total number of views for each channel
with st.expander("7 - What is the total number of views for each channel, and what are their corresponding channel names?"):
    result = session.query(ch.channel_name, ch.view_count).all()
    
    df = DataFrame(result)
    st.write(df)

# Query 8: Names of all channels that have published videos in the last month
with st.expander("8 - What are the names of all the channels that have published videos in the last month?"):
    result = session.query(
        ch.channel_name.label('Channel'), 
        v.published.label('Published')
    ).join(v, v.channel_id == ch.channel_id).filter(func.date_part('month', v.published) == func.date_part('month', func.now())).all()
    
    df = DataFrame(result)
    df_grouped = df.groupby('Channel').size().reset_index(name='Count of Videos')
    st.write(df_grouped)

# Query 9: Average duration of all videos in each channel
with st.expander("9 - What is the average duration of all videos in each channel, and what are their corresponding channel names?"):
    result = session.query(
        ch.channel_name.label('Channel'), 
        func.avg(func.extract('epoch', v.duration)).label('Average Duration (s)')
    ).join(v, v.channel_id == ch.channel_id).group_by(ch.channel_name).all()
    
    df = DataFrame(result)
    st.write(df)

# Query 10: Videos with the highest number of comments and their corresponding channel names
with st.expander("10 - Which videos have the highest number of comments, and what are their corresponding channel names?"):
    result = session.query(
        v.title.label('Video Name'), 
        v.comment_count.label('Comments'), 
        ch.channel_name.label('Channel'), 
        func.concat('https://www.youtube.com/watch?v=', v.video_id).label('Link')
    ).join(ch, v.channel_id == ch.channel_id).order_by(v.comment_count.desc()).limit(10).all()
    
    df = DataFrame(result)
    df_with_link(df, 'Video Name', 'Link')