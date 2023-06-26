import pandas as pd

csvFiles = ['data', 'media', 'place', 'pool', 'tweets', 'users']

for file in csvFiles:
  path = "twitter-csv/" + file + ".csv"
  data = pd.read_csv(path,delimiter=',',nrows=35000)

  # data.columns = data.columns.str.replace(r'.', '_')
  # data.rename(columns={'_id': 'item_id'}, inplace=True)

  newPath = "twitter-excel/" + file + ".xlsx" 
  # resultExcelFile = pd.ExcelWriter(newPath)

  data.to_excel(newPath, index=False)

