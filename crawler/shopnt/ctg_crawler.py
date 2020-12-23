import os

from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'snt_mall_category.html'), 'r') as f:
    page = f.read()

soup = BeautifulSoup(page, 'html.parser')

top_ctgs = soup.select('li.top_name')

for ctg in top_ctgs:
    # print(ctg.ul)
    try:
        bot_ctgs = ctg.ul.select('li')
    except:
        continue
    for b_btg in bot_ctgs:
        print(ctg.button.text, end='\t')
        a = b_btg.a
        print(a.text, end='\t')
        print(a['href'])

# links = soup.select('a')
# for link in links:
#     print(link)