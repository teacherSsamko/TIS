import os
import datetime
import csv
import re

from pymongo import MongoClient
from openpyxl import Workbook, load_workbook

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col_purchase = db['shopnt_purchase']

purchase_dir = '/Users/ssamko/Documents/ssamko/aircode/에어코드 제공 데이터/쇼핑엔티_20191101_20201031_주문데이터'
purchase_list = os.listdir(purchase_dir)

"""
purchase_dt: 주문일자
uid: 고객번호
gender: 성별(Male/Female/etc)
prod_id: 상품코드
prod_name: 상품명
prod_opt: 상품옵션
order_count: 주문수량
ship_count: 배송수량
cancle_count: 취소수량
order_id: 주문번호
order_sys: 주문매체
discount: 일시불할인
system: 매체
settop_id: 셋탑ID
refund_count: 반품수량
refund_reason: 반품사유
change_count: 교환횟수
coupon: 쿠폰사용금액
mileage: 적립금사용

"""

for f in purchase_list:
    print(f)
    with open(os.path.join(purchase_dir, f), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()
        for row in reader:
            print(row)
            data = {
                'purchase_dt': row[0],
                'uid': row[1],
                'gender': row[2],
                'prod_id': int(row[3]),
                'prod_name': row[4],
                'prod_opt': row[5],
                'order_count': int(row[6]),
                'ship_count': int(row[7]),
                'cancle_count': row[8],
                'order_id': int(row[9]),
                'order_sys': row[13],
                'discount': row[14],
                'system': row[15],
                'settop_id': row[16],
                'refund_count': row[17],
                'refund_reason': row[18],
                'change_count': row[19],
                'coupon': row[20],
                'mileage': row[21]
            }
            print(data)
            col_purchase.insert_one(data)
            # break
    # break


# i = 1
# r = []
# for row in ws.rows:
#     if i < 5:
#         i += 1
#         continue
#     for cell in row:
#         if cell.value: r.append(cell.value)

#     if i % 2 == 0:
#         print(r)
#         # insert data to DB here
#         on_time = r[-4].split(" ~ ")
#         print(on_time)
#         data = {
#             'on_date': r[1],
#             'start_time': on_time[0],
#             'end_time': on_time[1],
#             'play_period': r[-4],
#             'main': r[3] == 'O',
#             'prod_id': r[4],
#             'prod_name': r[5],
#             'prod_price': int(re.sub(',', '', r[6])),
#             'prod_stock': int(re.sub(',', '', r[-3])),
#             'prod_status': r[7],
#             'prod_ctg': r[-2],
#             'MD': r[8],
#             'supplier': r[-1],
#             'QA': r[9],
#             'gift_stockout': r[10] == 'Y',

#         }
#         print(data)
#         col_schedule.insert_one(data)
#         r = []
#     # if i == 10:
#     #     break
#     i += 1



# for row in ws.iter_rows():
#     for cell in row:
#         print(cell.value)
#         break
#     break



