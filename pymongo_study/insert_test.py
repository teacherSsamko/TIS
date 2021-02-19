from pymongo import MongoClient

mongo = MongoClient(f"mongodb://localhost:27017")
db = mongo['aircode']
col = db['w_reviews']

data = {
    'test':'how',
    'ids':1
}

col.insert_one(data)