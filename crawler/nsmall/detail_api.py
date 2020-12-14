import json

import requests

url = 'http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001'
data = {
    "cmdType":7,"catentryId":"30200279","busChnId":"CTCOM","deviceChnId":"INT"
}
result = requests.get(url, data)
print(result)
print(result.json())