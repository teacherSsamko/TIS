import csv
import os


from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_purchase']



# method 1
purchase_list = list(col.find())
# stids = set()

# for p in purchase_list:
#     stids.add(p['settop_id'])

# # print(stid)
# print(len(stids))

# method 2
stids = col.distinct("settop_id")


with open(os.path.join(BASE_DIR, 'data/settop_ids2.txt'), 'w') as f:
    f.write(f'{len(stids)}\n')
    for id in stids:
        f.write(f'{id}\n')

"""
result:
method1 make order randomly due to set
method2 more faster and less code
"""

