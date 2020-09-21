import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = 'https://www.shoppingntmall.com/display/goods/'

with open(os.path.join(BASE_DIR,'prod_id_list.txt'), 'r') as f:
    prods = f.readlines()

for prod_id in prods:
    url = url_prefix + prod_id
    print(url)
    driver.get(url)
    time.sleep(1)

    try:
        prod_name = driver.find_element_by_css_selector('div.new_good_name > span.tits').text
        print(prod_name)
        price = driver.find_element_by_css_selector('span.price_txt > span.num').text
        print(price)
        img_url = driver.find_element_by_css_selector('ul.swipe-wrap > li > img').get_attribute('src')
        print(img_url)
    except:
        prod_name = '페이지 없음'
        price = '0'
        img_url = 'https://img.shoppingntmall.com/goods/480/10011480_ss.jpg'
    
    try:
    # driver.find_element_by_css_selector('div.star_wrap').click()
    # print('click')
    # score = driver.find_element_by_css_selector('strong#commentTotalScore').text
        score = driver.find_element_by_css_selector('div.star_wrap > div > span').get_attribute('style').split(':')[-1].strip("%;")
        print(score)
        score_persons = driver.find_element_by_css_selector('div.star_wrap > span.num').text.strip("()")
        print(score_persons)
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
    }
    col.insert_one(db_data)

driver.quit()
