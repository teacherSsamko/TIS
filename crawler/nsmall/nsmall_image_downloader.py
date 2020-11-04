import os
import urllib.request
import datetime

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
# review_col = db['nsmall_reviews']
prod_col = db['nsmall']
today = datetime.date.today()

prod_list = list(prod_col.find('reg_date':str(today)))

for prod in prod_list:
    prod_id = prod['prod_id']
    img_url = prod['img_url']
    urllib.request.urlretrieve(img_url, f"crawler/nsmall/images/{prod_id}.jpg")