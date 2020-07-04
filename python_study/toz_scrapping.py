import requests

from selenium import webdriver
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome(executable_path="/Users/ssamko/Downloads/chromedriver")
url = 'https://community./13425'
driver.get(url)

soup = bs(driver.page_source, 'html.parser')

body_div = soup.select('#post_1 > div > div.topic-body.clearfix > div.regular.contents > div')

print(body_div)
for p in body_div:
    print(p)

driver.quit()