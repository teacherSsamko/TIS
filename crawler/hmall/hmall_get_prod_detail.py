import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient


options = Options()
options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['hmall_prod']

today = datetime.date.today()

with open(f'crawler/hmall/daily/{today}.txt','r') as f:
    urls = f.readlines()[20:]
    for url in urls:
        print(url)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        
        # with open('crawler/hmall/page_sample.txt','w') as sample:
        #     sample.write(data.text)
        prod_id = soup.select_one('div.pdtCode > span:nth-child(1)').text.split(":")[-1].strip()
        prod_id = int(prod_id)
        print(prod_id)
        prod_name = soup.select_one('h3.pdtTitle').text.strip()
        print(prod_name)
        price = soup.select_one('p.finalPrice.number.hasDC > strong').text.strip()
        print(price)
        try:
            score = soup.select_one('em.scoreMount').text.strip()
            print(score)
            score_persons = soup.select_one('p.scoreNum').text[1:].split()[0]
            print(score_persons)
        except:
            print('No score excists')
            score = None
            score_persons = 0
        img_url = soup.select_one('#prd_ipzoom > img')['src']
        # prd_ipzoom > div._frm_magnifier > div > img
        print(img_url)
        db_data = {
            'prod_id': prod_id,
            'prod_name': prod_name,
            'price': price,
            'score': score,
            'score_persons':score_persons,
            'img_url':img_url
        }
        col.insert_one(db_data)
        # time.sleep(2)
        # break