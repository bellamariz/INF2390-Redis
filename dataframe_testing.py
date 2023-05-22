import redis
import pandas as pd

redisConn = redis.Redis(
  host='redis-12746.c284.us-east1-2.gce.cloud.redislabs.com',
  port=12746,
  password='JYbSnXYUlb6DTjPEVLgynstCuh5J5Ot0')

dfUsers = pd.read_csv("twitter-csv/users.csv",delimiter=',',nrows=1000)
dfTweets = pd.read_csv("twitter-csv/tweets.csv",delimiter=',',nrows=1000)
dfPool = pd.read_csv("twitter-csv/pool.csv",delimiter=',',nrows=1000)
dfPlace = pd.read_csv("twitter-csv/place.csv",delimiter=',',nrows=1000)
dfMedia = pd.read_csv("twitter-csv/media.csv",delimiter=',',nrows=1000)
dfData = pd.read_csv("twitter-csv/data.csv",delimiter=',',nrows=1000)

dfUsers.columns = dfUsers.columns.str.replace(r'.', '_')
dfUsers.rename(columns={'_id': 'item_id'}, inplace=True)

dfTweets.columns = dfTweets.columns.str.replace(r'.', '_')
dfTweets.rename(columns={'_id': 'item_id'}, inplace=True)

dfPool.columns = dfPool.columns.str.replace(r'.', '_')
dfPool.rename(columns={'_id': 'item_id'}, inplace=True)

dfPlace.columns = dfPlace.columns.str.replace(r'.', '_')
dfPlace.rename(columns={'_id': 'item_id'}, inplace=True)

dfMedia.columns = dfMedia.columns.str.replace(r'.', '_')
dfMedia.rename(columns={'_id': 'item_id'}, inplace=True)

dfData.columns = dfData.columns.str.replace(r'.', '_')
dfData.rename(columns={'_id': 'item_id'}, inplace=True)

for row in dfTweets.itertuples(index=False):
  print(row,'\n')