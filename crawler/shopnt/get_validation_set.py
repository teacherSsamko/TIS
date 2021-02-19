import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

url = 'http://localhost:5000/rec_prod'

params = '엘리자베스아덴 선글라스 쥬얼에디션'

with open(os.path.join())

res = requests.get(url, params=params).json()

goods = res['goods_code']

for p in goods:
    print(p['prod_id'])