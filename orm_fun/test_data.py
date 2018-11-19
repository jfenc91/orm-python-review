import json
import pandas as pd

with open("../wine-reviews/winemag-data-130k-v2.json") as f:
    data = json.loads(f.read())


#,country,
# description,designation,points,price,province,region_1,region_2,taster_name,
# taster_twitter_handle,title,variety,winery




pd = pd.read_csv("../wine-reviews/winemag-data-130k-v2.csv")
print(pd.groupby('title').groups)
