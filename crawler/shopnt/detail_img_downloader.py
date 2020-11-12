import os
import datetime
import urllib.request

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

today = datetime.date.today()

prod_list = list(col.find({}))

dir_name = 'detail_images'

if not os.path.exists(os.path.join(BASE_DIR, dir_name)):
    os.mkdir(os.path.join(BASE_DIR, dir_name))

if not os.path.exists(os.path.join(BASE_DIR, f'{dir_name}/{today}')):
    os.mkdir(os.path.join(BASE_DIR, f'{dir_name}/{today}'))

i = 0

# total = len(prod_list) - stop - 1
total = len(prod_list)

for prod in prod_list:
    i = prod_list.index(prod)
    try:
        urls = prod['detail_imgs_url']
    except:
        print('url error')
        i += 1
        continue
    if urls:
        img_idx = 0
        for url in urls:
            if prod['prod_id'][:-2] != '':
                prod_id = prod['prod_id'][:-1]
                print(prod_id)
                prod_id = int(prod_id)
                try:
                    urllib.request.urlretrieve(url, os.path.join(BASE_DIR,f"{dir_name}/{today}/{prod_id}_{img_idx}.jpg"))
                except:
                    print('image cannot load')
                    continue
                img_idx += 1
    else:
        print("no detail imgs")
    print(f'{i}/{total}')
