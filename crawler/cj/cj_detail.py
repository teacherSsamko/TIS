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
col = db['cj_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open(f'crawler/cj/daily/{today}/url_list.txt','r') as f:
    urls = f.readlines()

for url in urls:
    driver.get(url)
    time.sleep(2)
    prod_id = url.split("?")[0].split("/")[-1]
    try:
        prod_name= driver.find_element_by_css_selector('h3.prd_tit').text.strip()
        price = driver.find_element_by_css_selector('span.price_txt > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('div#_topPrdImg > img').get_attribute('src')
    
    try:
        score = driver.find_element_by_css_selector('#_MENTION > div.review_summary > div > div > div > span').get_attribute('style').split(":")[-1].split("%")[0]
        print(score)
        score_persons = driver.find_element_by_css_selector('p.score_noti > strong').text[:-1]
    except:
        score = None
        score_persons = 0
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': score,
        'score_persons': score_persons,
        'img_url':img_url,
        'reg_date':today
    }
    print(prod_id)
    print(prod_name)
    print()
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()