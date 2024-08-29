import googleapiclient.discovery
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
yt_api_key = os.environ.get('yt_api_key') 


class yt:
    def __init__(self):
        self.yt = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=yt_api_key)
        

    def getChDetails(self, chId):
        request = self.yt.channels().list(
                part="snippet,contentDetails,statistics",
                id=chId
            )
        r = request.execute()
        gotInfo = r['pageInfo']['totalResults']
        if gotInfo:
            chDetails = {
                'channel_id': chId,
                'channel_name': r['items'][0]['snippet']['title'],
                'channel_desc': r['items'][0]['snippet']['description'],
                'username': r['items'][0]['snippet']['customUrl'],
                'published': r['items'][0]['snippet']['publishedAt'],
                'thumbnail': r['items'][0]['snippet']['thumbnails']['high']['url'],
                'videos_id': r['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                'view_count': int(r['items'][0]['statistics']['viewCount']),
                'sub_count': int(r['items'][0]['statistics']['subscriberCount']),
                'vid_count': int(r['items'][0]['statistics']['videoCount'])
            }

            return chDetails
        else: return -1


    def getVideos(self, videosId):
        # nextPageToken = ['']

        request = self.yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=videosId,
            maxResults=300,
            # nextPageToken = nextPageToken[-1]
        )

        # while len(vids) < 301:
        res = request.execute()
        
        request = self.yt.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(i['contentDetails']['videoId'] for i in res['items'])
        )
        
        res = request.execute()
        vids = res['items'] 
        videos = []
        
        for j in range(len(vids)):
            i = vids[j]
            videos.append({
                'video_id': i['id'],
                'published': i['snippet']['publishedAt'],
                'channel_id': i['snippet']['channelId'],
                'title': i['snippet']['title'],
                'thumbnail': i['snippet']['thumbnails']['standard']['url'],
                'category_id': i['snippet']['categoryId'],
                'duration': i['contentDetails']['duration'].replace('PT', ''),#.split('M')[0]
                'view_count': int(i['statistics']['viewCount']),
                'like_count': int(i['statistics']['likeCount']),
                'comment_count': int(i['statistics'].get('commentCount', 0)),
            })

        return videos

    
    def getCategories(self):
        request = self.yt.videoCategories().list(
            part="snippet",
            regionCode="US"
        )
        response = request.execute()
        cats = {}
        for i in response['items']:
            cats[i['id']] = i['snippet']['title']
        return cats
    

    def getComments(self, vId):
        request = self.yt.commentThreads().list(
            part="snippet",
            videoId=vId,
        )
        response = request.execute()
        comments = []

        for i in response['items']:
            comments.append({
                    'comment_id': i['id'],
                    'channel_id': i['snippet']['channelId'],
                    'video_id': i['snippet']['topLevelComment']['snippet']['videoId'],
                    'text_display': i['snippet']['topLevelComment']['snippet']['textDisplay']
                })

        return comments