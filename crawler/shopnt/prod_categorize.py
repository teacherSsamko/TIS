import os
import csv
import datetime

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']


today = datetime.date.today()
prod_list = list(col.find({'top_ctg':{"$exists":True}}, {'_id':False}))

"""
row를 돌면서 
prod_id와 매칭되는 document에 
update categories 
"""

with open("categorized_snt.tsv", 'w') as f:
    for prod in prod_list:
        for v in prod.values():
            f.write(f'{v}\t')
        f.write('\n')

# unlabeled = ['10095254', '10095253', '10167038', '10099849', '10153142',
#        '10094652', '10055435', '10228858', '10151326', '10095252',
#        '10094659', '10094658', '10151333', '10116465', '10207075',
#        '10081135', '10151328', '10114953', '10224928', '10240955',
#        '10190401', '10098866', '10209690', '10033400', '10210255',
#        '10098499', '10094651', '10116219', '10210597', '10156008',
#        '10241025', '10166104', '10117934', '10207074', '10025443',
#        '10229169', '10088109', '10210598', '10095251', '10167000',
#        '10162884', '10245321', '10210971', '10226637', '10036337',
#        '10231312', '10179069', '10216646', '10103464', '10155020',
#        '10082945', '10103466', '10095190', '10229170', '10224817',
#        '10103950', '10101736', '10103467', '10099789', '10108088']

# with open(os.path.join(BASE_DIR,"SNT_goods_catogory_final_v1.0.csv"),newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=",")
#     reader.__next__
#     for row in reader:
#         prod_id = f'{row[2]}\n'
#         top_ctg = row[0]
#         bot_ctg = row[1]
#         doc = {
#             "top_ctg":top_ctg,
#             "bot_ctg":bot_ctg
#         }
#         col.find_one_and_update({"prod_id":str(prod_id)}, {"$set":doc})

# with open(os.path.join(BASE_DIR,"SNT_goods_catogory_final_v1.0.csv"),newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=",")
#     reader.__next__

# for prod_id in unlabeled:
#     data = col.find_one({'prod_id':prod_id})
#     prod_name = data['prod_name']

