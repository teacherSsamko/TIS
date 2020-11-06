import os
import urllib.request
import datetime

from pymongo import MongoClient


def main():
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    mongo = MongoClient("mongodb://localhost:27017")
    db = mongo['aircode']
    # review_col = db['nsmall_reviews']
    prod_col = db['nsmall']
    today = datetime.date.today()

    prod_list = list(prod_col.find({'reg_date':str(today)}))

    if not os.path.exists(os.path.join(BASE_DIR, f'images/{today}')):
        os.mkdir(os.path.join(BASE_DIR, f'images/{today}'))

    img_dir = os.path.join(BASE_DIR, 'images')

    total = len(prod_list)
    i = 1

    for prod in prod_list:
        print(f'{i}/{total}')
        prod_id = prod['prod_id']
        img_url = prod['img_url']
        urllib.request.urlretrieve(img_url, f"{img_dir}/{today}/{prod_id}.jpg")
        i += 1