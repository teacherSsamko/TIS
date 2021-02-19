from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

id_list = list(col.find({'prod_name':'페이지 없음'},{'prod_id':True, '_id':False}))
print(id_list)

with open('crawler/shopnt/invalid_ids.csv', 'w') as f:
    for pid in id_list:
        f.write(f'{pid["prod_id"]},')