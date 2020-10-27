import os
import datetime
import urllib.request

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

today = datetime.date.today()

prod_list = list(col.find({'reg_date':'2020-10-07'}))

if not os.path.exists(os.path.join(BASE_DIR, 'images')):
    os.mkdir(os.path.join(BASE_DIR, 'images'))

if not os.path.exists(os.path.join(BASE_DIR, f'images/{today}')):
    os.mkdir(os.path.join(BASE_DIR, f'images/{today}'))

i = 0
stop = 236 + 247 + 31 + 197 + 153 + 32 + 183 + 15
# total = len(prod_list) - stop - 1
total = len(prod_list)

for prod in prod_list:
    img_url = prod['img_url']
    if prod['prod_id'][:-2] != '':
        prod_id = prod['prod_id'][:-2]
        print(prod_id)
        prod_id = int(prod_id)
        urllib.request.urlretrieve(img_url, os.path.join(BASE_DIR,f"images/{today}/{prod_id}.jpg"))
        print(f'{i}/{total}')
    i += 1