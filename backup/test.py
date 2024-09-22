from util.yt_sql import sql, YtChannelModel, YtVideosModel, YtCommentsModel
print(1)
session = sql()
print(2)

session.query(YtChannelModel).delete()
print(3)

session.query(YtVideosModel).delete()
print(4)

session.query(YtCommentsModel).delete()
print(5)