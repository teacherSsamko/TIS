from pymongo import MongoClient, WriteConcern

# from ..python_study.config.config import Config
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from python_study.config.config import Config
    else:
        from ..python_study.config.config import Config

mongo_ip = Config().MONGO_REMOTE_HOST
print(mongo_ip)

uriString = f'mongodb://{mongo_ip}'

client = MongoClient(uriString)
wc_majority = WriteConcern("majority", wtimeout=1000)

client.get_database("examples", write_concern=wc_majority).inventory.insert_one({'name':'ssamko'})