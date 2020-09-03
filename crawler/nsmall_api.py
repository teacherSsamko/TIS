import os

import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
collection = db['nsmall']

pCatalogId = '72001'
pCatgroupIdChild = '1259564'
# pListId는 카테고리
parent_dom = requests.get(url='http://www.nsmall.com/NSTvThemeView?storeId=13001&langId=-9&catalogId=72001&catgroupId=1174555')
# for pPage in range(1,7):
parent_soup = BeautifulSoup(parent_dom.text, 'html.parser')
db_dataset = []
with open('crawler/nsmall/item_list.txt','w') as f:
    for pListId in range(2,5):
    # for pListId in range(1,2):
        ctg_name = parent_soup.select_one(f'#themeTempCat{pListId}').text
        f.write(f'[ {ctg_name} ]\n\n')
        
        for pPage in range(1,7):
            
            # pListId = 1
            # pPage = 1
            data = { 'catalogId' : pCatalogId, 'catgroupIdChild' : pCatgroupIdChild, 'listId' : pListId, 'page' : pPage }
            result = requests.post(url="http://www.nsmall.com/TvThemePrdtList?storeId=13001&langId=-9", data=data)
            print(result)
            soup = BeautifulSoup(result.text, 'html.parser')
            # print(f'#themeTempCat{pListId}')
            
            print(ctg_name)
            
            item_list = soup.select('#List > ul')
            for ul in item_list:
                for item in ul.select('li'):
                    print(f'page {pPage}')
                    prod_name = item.select_one('dt').text
                    print(prod_name)
                    f.write(f"{prod_name}\n")
                    # db_data['prod_name'] = prod_name
                    print(f'{item.a["href"]}')
                    item_href = 'http://www.nsmall.com'+item.a["href"][1:]
                    f.write(f'{item_href}\n')
                    # db_data['prod_detail_url'] = item_href
                    # item detail page
                    item_detail = requests.get(url=item_href)
                    detail_soup = BeautifulSoup(item_detail.text, 'html.parser')
                    # print(detail_soup)
                    prod_id = item_href.split("=")[4].split("&")[0]
                    f.write(f'id: {prod_id}\n')
                    # db_data['prod_id'] = int(prod_id)
                    price = detail_soup.select_one('strong.save_price > em').text
                    f.write(f'price: {price}\n')
                    # db_data['prod_price'] = price
                    try:
                        score = detail_soup.select_one('span.str_count > strong').text
                        score_persons = detail_soup.select_one('span.str_count > span').text.strip("()")
                    except:
                        score, score_persons  = 'None', 'None'
                    f.write(f'score: {score}\n')
                    # db_data['score'] = score
                    f.write(f'score_persons: {score_persons}\n')
                    # db_data['score_persons'] = score_persons
                    # detail_img = detail_soup.select_one('#dvGoodsGuideDataList > p:nth-child(2)').img['src']
                    # print(detail_img)
                    # f.write(f'detail_img: {detail_img}\n')
                    print(f"http:{item.img['src']}")
                    f.write(f"http:{item.img['src']}\n")
                    # db_data['img_url'] = item.img['src']
                    f.write('\n')
                    db_data = {
                        'ctg':ctg_name,
                        'prod_id':int(prod_id),
                        'prod_name':prod_name,
                        'prod_price':price,
                        'score':score,
                        'score_persons':score_persons,
                        'img_url':f'http:{item.img["src"]}'
                    }
                    db_dataset.append(db_data)

# with open('crawler/nsmall/db_set.txt','w') as f:
#     f.write("\n".join(db_dataset))

collection.insert_many(db_dataset)


