import csv
import redis
import unidecode
import json
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

global redisConn, pipe, conf

redisConn = redis.Redis(
  host="localhost",
  port=10001)

pipe = redisConn.pipeline()

def build_dictionary(file_name):
  dataset = {file_name : list()}
  column_names = list()
  item = dict()

  # read csv file
  # ex: places.csv
  with open("twitter-csv/"+file_name+".csv", 'r') as file:
    csvreader = csv.reader(file)

    # for each row in csv file
    for i,row in enumerate(csvreader):
      # max number of rows to insert to database
      if i==50000:
        break

      # first row: dataset's column names
      # ex: _id	country	country_code	full_name	geo.bbox	geo.properties	geo.type	id	name	place_type
      if i == 0:
        column_names = row
        continue

      # next rows: actual data
      # ex: 3bcc0c	Brasil	BR	Boa Vista, Brasil	[-61.000632,2.427858,-60.2877575,3.606091]	[object Object]	Feature	ef4296e721b70dfe	Boa Vista	city
      item = {}

      # for each row, map its attributes to their respective column names
      # use unidecode to remove accents (not accepted by redis)
      # ex: dataset = { "places": [ {"_id":"3bcc0c", "country":"Brasil", ...}, {"_id":"abcj73", "country":"Estados Unidos", ...}, ... ] }
      for j,attr in enumerate(row):
        item[str(column_names[j])] = unidecode.unidecode(str(attr))

      dataset[file_name].append(item)
  
  return dataset

def populate_redis_as_json(file_name):
  global pipe
  dataset = build_dictionary(file_name)

  for idx,data in enumerate(dataset[file_name]):
    pipe.json().set(file_name+':'+str(idx), '$', data)

def populate_redis(file_name):
  global pipe
  dataset = build_dictionary(file_name)

  for idx,data in enumerate(dataset[file_name]):
    for column in data:
      pipe.hset(file_name+':'+str(idx), column, data[column])

# populate_redis("media")

index = "idx:user"
index_def = IndexDefinition(prefix=["user:"])
schema = (
    NumericField("id"),
    TextField("username"),
    NumericField("public_metrics.followers_count")
)
pipe.ft(index).create_index(schema, definition=index_def)
print(pipe.ft(index).info())

# FT.CREATE idx:user ON hash PREFIX 1 "users:" SCHEMA id NUMERIC SORTABLE username TEXT SORTABLE public_metrics.followers_count NUMERIC SORTABLE

pipe.execute()
