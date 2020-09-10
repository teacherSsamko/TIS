import os
import urllib.request
import datetime
import time

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['w_prod']

prods = list(col.find())

today = datetime.date.today()

if not os.path.exists(f'crawler/w/images/{today}'):
    os.mkdir(f'crawler/w/images/{today}')

for prod in prods:
    url = prod['img_url']
    urllib.request.urlretrieve(url, f"crawler/w/images/{today}/{prod['prod_id']}.jpg")