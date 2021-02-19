import os
import sys
import csv
import datetime

from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

conf = Config()
print(conf.MONGO_REMOTE_IP)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
db = mongo['aircode']
col = db['shopnt_settop']
col_purchase = db['shopnt_purchase']

# with open(os.path.join(BASE_DIR, 'data/settop_ids2.txt'), 'r') as f:
#     stids = csv.reader(f, delimiter='\n')
#     stids.__next__()
#     for id in stids:
#         data = {
#             'stid':id
#         }
#         col.insert_one(data)

# purchase_list = list(col_purchase.find())
# order_list = {}

# for p in purchase_list:
#     # update_set = {
#     #     'gender':p['gender'],
#     # }
#     # col.find_one_and_update({'stid':p['settop_id']}, {'$set': update_set})
    
#     data = {
#         'prod_id':p['prod_id'],
#         'prod_name': p['prod_name'],
#         'order_count': p['order_count'],
#         'cancel_count': p['cancle_count']
#     }
#     # if order_list.get(p['settop_id']):
#     #     order_list[p['settop_id']].append(data)
#     # else:
#     #     order_list[p['settop_id']] = [data]
#     col.update_one({'stid':p['settop_id']}, {'$push':{'order':data}})
#     # print(p['settop_id'])

# print(order_list)

settops = list(col.find())
print(len(settops))
start_t = datetime.datetime.now()
i = 1
for settop in settops:
    stid = settop['stid'][0]
    gender = col_purchase.find_one({'settop_id':stid})['gender']
    col.find_one_and_update({'stid':[stid]}, {'$set':{'gender':gender}})
    if i % 100 == 0:
        tmp_t = datetime.datetime.now()
        print(f"{i} - runtime: {tmp_t - start_t}")
    i += 1

end_t = datetime.datetime.now()
print(f"finish\nruntime: {end_t - start_t}")

