import re
import json

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']
col_review = db['shopnt_review']

prod_list = list(col.find({'prod_name':{'$not':re.compile('페이지 없음')}}))

# options = Options()
# options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = 'https://www.shoppingntmall.com/display/goods/'
prod_id = '10243188'
p = 1

best_comments = f'http://www.shoppingntmall.com/comment/list-html?goodsCode={prod_id}&rowsPerPageComment=100&currentPageComment={p}&specialDisplayYn=1&commentSort=1&commentCode=&null&_=1608616226353'

total = len(prod_list[2315:])

for i, prod in enumerate(prod_list[2315:]):
    print(f'\r{i}/{total}', end='')
    prod_id = prod['prod_id'].strip()
    norm_comments = f'http://www.shoppingntmall.com/comment/list-html?goodsCode={prod_id}&rowsPerPageComment=100&currentPageComment={p}&commentCode=&commentSort=1&null&_=1608615874142'
    best_comments = f'http://www.shoppingntmall.com/comment/list-html?goodsCode={prod_id}&rowsPerPageComment=100&currentPageComment={p}&specialDisplayYn=1&commentSort=1&commentCode=&null&_=1608616226353'
    # driver.get(url)
    # WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#goodsDetail')))
    norm = requests.get(norm_comments).json()
    best = requests.get(best_comments).json()
    # norm = 
    normList = norm['commentList']
    bestList = best['commentList']

    p = 1
    while normList:
        for cmt in normList:
            doc = {
                'prod_id':prod_id,
                'prod_name':prod['prod_name'],
                'score': cmt['commentScore'],
                'review': cmt['commentContent'],
                'orderNo': cmt['orderNo'],
                'goodsDtInfo': cmt['goodsDtInfo'],
                'receiveMethod': cmt['receiveMethod']
            }
            # print(doc)
            col_review.insert_one(doc)
        p += 1
        norm_comments = f'http://www.shoppingntmall.com/comment/list-html?goodsCode={prod_id}&rowsPerPageComment=100&currentPageComment={p}&commentCode=&commentSort=1&null&_=1608615874142'
        norm = requests.get(norm_comments).json()
        normList = norm['commentList']
        # print('here')

    p = 1
    while bestList:
        # print('1')
        for cmt in bestList:
            doc = {
                'prod_id':prod_id,
                'prod_name':prod['prod_name'],
                'score': cmt['commentScore'],
                'review': cmt['commentContent'],
                'orderNo': cmt['orderNo'],
                'goodsDtInfo': cmt['goodsDtInfo'],
                'receiveMethod': cmt['receiveMethod']
            }
            # print(doc)
            col_review.insert_one(doc)
        p += 1
        best_comments = f'http://www.shoppingntmall.com/comment/list-html?goodsCode={prod_id}&rowsPerPageComment=100&currentPageComment={p}&specialDisplayYn=1&commentSort=1&commentCode=&null&_=1608616226353'
        best = requests.get(best_comments).json()
        bestList = best['commentList']
    # print(best['totalCount'])
    # print(best['commentList'][0])
    # print('2')
    # break
print('3')