import os
import urllib.request

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['ssg_prod']

prod_list = list(col.find())

# with open(f"crawler/ssg/videos/{directory}/url_list.txt", 'r') as f:
#     urls = f.readlines()
#     i = 0
#     for url in urls:
#         urllib.request.urlretrieve(url, f"./images/{directory}/{i}.jpg")
#         i += 1

for prod in prod_list:
    try:
        video_url = prod['video_url']
        prod_id = prod['prod_id']
        print(prod_id)
    except:
        continue
    print('start download')
    urllib.request.urlretrieve(video_url, f"crawler/ssg/videos/{prod_id}.mp4")
    print('download finisehd')