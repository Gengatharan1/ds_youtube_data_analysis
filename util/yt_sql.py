from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime,
    MetaData, BigInteger
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
username = os.environ.get('sql_db_usr') 
password = os.environ.get('sql_db_pwd')
hostname = os.environ.get('sql_host')
port = os.environ.get('sql_db_endpoint')
database = os.environ.get('sql_db_dbname')

# postgresql
db_url = f'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'

# # mysqlclient
# username = os.environ.get('sql_db_usr') 
# password = os.environ.get('sql_db_pwd')
# hostname = os.environ.get('sql_host')
# database = os.environ.get('sql_db_dbname')

# db_url = f'mysql+mysqldb://{username}:{password}@{hostname}/{database}'

db_channels_coll_name = os.environ.get('db_channels_coll_name')
db_videos_coll_name = os.environ.get('db_videos_coll_name')
db_comments_coll_name = os.environ.get('db_comments_coll_name')

# Create engine
engine = create_engine(db_url)

# Create a base class for your ORM models
Base = declarative_base()

# Define your ORM model
class YtChannelModel(Base):
    __tablename__ = db_channels_coll_name

    channel_id = Column(String, primary_key=True)
    channel_name = Column(String)
    channel_desc = Column(String)
    username = Column(String)
    published = Column(DateTime)
    thumbnail = Column(String)
    country = Column(String)
    videos_id = Column(String)
    view_count = Column(BigInteger)
    sub_count = Column(BigInteger)
    vid_count = Column(BigInteger)

class YtVideosModel(Base):
    __tablename__ = db_videos_coll_name

    video_id = Column(String, primary_key=True)
    published = Column(DateTime)
    channel_id = Column(String)
    title = Column(String)
    thumbnail = Column(String)
    category_id = Column(String)
    duration = Column(String)
    view_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)

class YtCommentsModel(Base):
    __tablename__ = db_comments_coll_name

    comment_id = Column(String, primary_key=True)
    channel_id = Column(String)
    video_id = Column(String)
    text_display = Column(String)


def sql():
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()
    return session