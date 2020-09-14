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
col = db['sk_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "http://www.skstoa.com/display/goods/"

with open('crawler/sk/prod_id_list.txt','r') as f:
    prod_ids = f.readlines()[1207:]

for prod_id in prod_ids:
    prod_id = prod_id.replace("\n","")
    if len(prod_id) == 8:
        url = url_prefix + prod_id
    else:
        url = url_prefix + "deal/" + prod_id
    driver.get(url)
    time.sleep(2)
    try:
        prod_name= driver.find_element_by_css_selector('div.cont_tit > div.upper.clearfix > div.l_part').text
        price = driver.find_element_by_css_selector('p.price > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('img#goodsImg').get_attribute('src')
    try:
        video_url = driver.find_element_by_css_selector('video.vod > source').get_attribute('src')
    except:
        video_url = None
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': None,
        'score_persons': 0,
        'img_url':img_url,
        'video_url':video_url
    }
    print(prod_id)
    print(prod_name)
    print()
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()