from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']


prod_list = list(col.find())

total = len(prod_list)

for i, prod in enumerate(prod_list):
    print(f'\r{i} / {total}', end='')
    _id = prod['_id']
    origin_prod_id = prod['prod_id']
    new_prod_id = origin_prod_id.strip()
    
    col.find_one_and_update({'prod_id':origin_prod_id},{'$set':{'prod_id':new_prod_id}})
