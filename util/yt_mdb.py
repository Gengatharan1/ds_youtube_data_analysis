from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
db_channels_coll_name = os.environ.get('db_channels_coll_name')
db_videos_coll_name = os.environ.get('db_videos_coll_name')
db_comments_coll_name = os.environ.get('db_comments_coll_name')
mdb_dbName = os.environ.get('mdb_dbName')
mdb_usr = os.environ.get('mdb_usr')
mdb_pwd = os.environ.get('mdb_pwd')
mdb_appName = os.environ.get('mdb_appName')


class mdb():
    def __init__(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = 'mongodb+srv://'+mdb_usr+':'+mdb_pwd+'@test.s6wolmk.mongodb.net/?retryWrites=true&w=majority&appName='+mdb_appName
        # Create a new client and connect to the server
        self.client = MongoClient(CONNECTION_STRING, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print(e)

    def get_coll_channels(self):
        return self.client[mdb_dbName][db_channels_coll_name]
    
    def get_coll_videos(self):
        return self.client[mdb_dbName][db_videos_coll_name]
    
    def get_coll_comments(self):
        return self.client[mdb_dbName][db_comments_coll_name]