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

detail_img_api = 'http://www.shoppingntmall.com/display/goods/detail/describe/{prod_id}'

today = datetime.date.today()

with open(os.path.join(BASE_DIR,'unknown.txt'), 'r') as f:
    prods = f.readlines()
    # prods = list(map(lambda url: url.split("/")[-1], prods))
    total = len(prods)
current = 1
for i, prod_id in enumerate(prods):
    isExist = True
    url = url_prefix + prod_id.strip()

    print(f'{current}/{total}')
    # print(url)
    driver.get(url)
    time.sleep(1)

    try:
        prod_name = driver.find_element_by_css_selector('div.new_good_name > span.tits').text
        print(prod_name)
    except:
        isExist = False
        prod_name = '페이지 없음'
        print(url)
    try:
        price = driver.find_element_by_css_selector('span.price_txt > span.num').text
    except:
        price = '0'
    try:
        img_url = driver.find_element_by_css_selector('ul.swipe-wrap > li > img').get_attribute('src')
    except:
        img_url = 'https://img.shoppingntmall.com/goods/480/10011480_ss.jpg'
    detail_imgs_url = []
    try:
        detail_imgs = driver.find_elements_by_css_selector('#goods_describe > div > div > p > img')
        for img in detail_imgs:
            detail_imgs_url.append(img.get_attribute('src'))
    except:
        pass
    
    try:
    # driver.find_element_by_css_selector('div.star_wrap').click()
    # print('click')
    # score = driver.find_element_by_css_selector('strong#commentTotalScore').text
        score = driver.find_element_by_css_selector('div.star_wrap > div > span').get_attribute('style').split(':')[-1].strip("%;")
        score_persons = driver.find_element_by_css_selector('div.star_wrap > span.num').text.strip("()")
    except:
        score = None
        score_persons = 0
    

    db_data = {
        # 'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': score,
        'score_persons': score_persons,
        'img_url':img_url,
        'detail_img_url':detail_imgs_url,
        'reg_date': str(today)
    }
    # col.insert_one(db_data)
    col.find_one_and_update({'prod_id':prod_id},{'$set':db_data})
    current += 1

driver.quit()
