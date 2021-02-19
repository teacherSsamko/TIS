import os
import sys

from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.config import Config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

conf = Config()
# mongo = MongoClient(host=f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
mongo = MongoClient(host=f"mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_settop']

stids_info = list(col.find())

with open(os.path.join(BASE_DIR, 'data/sentence_from_settop.txt'), 'w') as f:
    for info in stids_info:
        sentence = ""
        stid = info['stid'][0]
        sentence += f"{stid}/셋탑아이디 "
        gender = info['gender']
        sentence += f"{gender}/성별 "
        orders = info['order']
        for order in orders:
            sentence += f"{order['prod_id']}/상품코드 "
            sentence += f"{order['prod_name']}/상품명 "
        f.write(f'{sentence}\n')
