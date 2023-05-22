import csv
import redis
import unidecode

redisConn = redis.Redis(
  host='redis-12746.c284.us-east1-2.gce.cloud.redislabs.com',
  port=12746,
  password='JYbSnXYUlb6DTjPEVLgynstCuh5J5Ot0')

# format column names
# dfData = pd.read_csv("twitter-csv/place.csv",delimiter=',',nrows=10)
# dfData.columns = dfData.columns.str.replace(r'.', '_')
# dfData.rename(columns={'_id': 'item_id'}, inplace=True)
# columns = dfData.columns.to_list()

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
      # first row: dataset's column names
      # ex: _id	country	country_code	full_name	geo.bbox	geo.properties	geo.type	id	name	place_type
      if i == 0:
        column_names = row
        continue

      # next rows: actual data
      # ex: 3bcc0c	Brasil	BR	Boa Vista, Brasil	[-61.000632,2.427858,-60.2877575,3.606091]	[object Object]	Feature	ef4296e721b70dfe	Boa Vista	city
      item = {}

      # for each row, map its attributes to their respective column names
      # ex: dataset = { "places": [ {"_id":"3bcc0c", "country":"Brasil", ...}, {"_id":"abcj73", "country":"Estados Unidos", ...}, ... ] }
      for j,attr in enumerate(row):
        item[str(column_names[j])] = unidecode.unidecode(str(attr))

      dataset[file_name].append(item)
  
  return dataset

def populate_redis(file_name):
  dataset = build_dictionary(file_name)

  for idx,data in enumerate(dataset[file_name]):
    redisConn.hmset(file_name+":id:"+str(idx), data)

csvFiles = ['data', 'media', 'place', 'pool', 'tweets', 'users']

populate_redis("users")

# ex: "place:id:1" -> [ "_id" -> "3bcc0c", "country" -> "Brasil", ... ]

# redis-cli -u redis://default:JYbSnXYUlb6DTjPEVLgynstCuh5J5Ot0@redis-12746.c284.us-east1-2.gce.cloud.redislabs.com:12746