import os
import time
import datetime
import sys

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import config

def main():
    conf = config.Config()


    options = Options()
    options.page_load_strategy = 'eager'
    # driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

    mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
    db = mongo['aircode']
    col = db['hmall_prod']

    today = datetime.date.today()

    with open(f'crawler/hmall/daily/{today}.txt','r') as f:
        urls = f.readlines()
        for url in urls:
            # print(url)
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            
            # with open('crawler/hmall/page_sample.txt','w') as sample:
            #     sample.write(data.text)
            try:
                prod_id = soup.select_one('div.pdtCode > span:nth-child(1)').text.split(":")[-1].strip()
                prod_id = int(prod_id)
                # print(prod_id)
                prod_name = soup.select_one('h3.pdtTitle').text.strip()
                # print(prod_name)
                price = soup.select_one('p.finalPrice.number.hasDC > strong').text.strip()
                # print(price)
            except:
                continue
            try:
                score = soup.select_one('em.scoreMount').text.strip()
                # print(score)
                score_persons = soup.select_one('p.scoreNum').text[1:].split()[0]
                # print(score_persons)
            except:
                print('No score excists')
                score = None
                score_persons = 0
            img_url = soup.select_one('#prd_ipzoom > img')['src']
            # prd_ipzoom > div._frm_magnifier > div > img
            # print(img_url)
            # 3 types of img path
            t1 = soup.select('#guidance > table > tbody > tr > td > p')
            t2 = soup.select('#deal_unit_d1 > dt > p')
            t3 = soup.select('#section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p')

            if t1:
                # print("t1 >>",t1)
                detail_imgs_p = t1
            elif t2:
                # print("t2 >>",t2)
                detail_imgs_p = t2
            elif t3:
                # print("t3 >>",t3)
                detail_imgs_p = t3
            else:
                print(t1, t2, t3)
                print('weird type error')
                continue
            detail_urls = []
            for p in detail_imgs_p:
                detail_img = p.select_one('img')
                if not detail_img:
                    continue
                # print('detail >>', detail_img['src'])
                # detail_img_url = detail_img['src']
                # print(type(detail_img_url))
                detail_urls.append(detail_img['src'])
                # print(detail_urls)
            
            # print(detail_urls[0][0][0][0][0])
            #['src']
            #guidance > table > tbody > tr > td > p:nth-child(1) > img
            #guidance > table > tbody > tr > td > p:nth-child(2) > img
            #guidance > table > tbody > tr > td > p:nth-child(2) > img
            #guidance > table > tbody > tr > td > p:nth-child(6) > img
            #guidance > table > tbody > tr > td > p:nth-child(2) > img
            #guidance > table > tbody > tr > td > p:nth-child(4) > img
            #guidance > table > tbody > tr > td > p:nth-child(2) > img
            #deal_unit_d1 > dt > p:nth-child(5) > img
            #deal_unit_d1 > dt > p:nth-child(3) > img
            #deal_unit_d1 > dt > p:nth-child(2) > img
            #deal_unit_d1 > dt > p:nth-child(7) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(5) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(5) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(3) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(2) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(1) > img
            #section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p:nth-child(3) > img

            db_data = {
                'prod_id': prod_id,
                'prod_name': prod_name,
                'price': price,
                'score': score,
                'score_persons':score_persons,
                'img_url':img_url,
                'detail_img_url':detail_urls,
                'reg_date':str(today)
            }
            col.insert_one(db_data)
            # print(db_data)
            # time.sleep(2)
            # break