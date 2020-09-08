from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
review_col = db['nsmall_reviews']
prod_col = db['nsmall']

print(review_col.estimated_document_count())