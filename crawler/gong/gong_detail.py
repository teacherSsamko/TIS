import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['gong_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "https://www.gongyoungshop.kr/goods/selectGoodsDetail.do?prdId="

with open('crawler/gong/prod_id_list.txt','r') as f:
    prod_ids = f.readlines()

total = len(prod_ids)
current = 1

for prod_id in prod_ids:
    print(f"{current} / {total}")
    prod_id = prod_id.replace("\n","")
    url = url_prefix + prod_id
    driver.get(url)
    time.sleep(2)
    try:
        prod_name= driver.find_element_by_css_selector('strong.goodsName').text
        price = driver.find_element_by_css_selector('p.afterPrice > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('img#zoomSnap').get_attribute('src')
    try:
        score = driver.find_element_by_css_selector('strong.starScore').text[:-1]
        score_persons = driver.find_element_by_css_selector('span.reviewCount > a').text[:-1]
    except:
        score = None
        score_persons = 0
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': score,
        'score_persons': score_persons,
        'img_url':img_url
    }
    print(prod_id)
    print(prod_name)
    print()
    col.insert_one(db_data)
    current += 1
    # break
    # time.sleep(2)

driver.quit()