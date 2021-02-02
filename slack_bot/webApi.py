import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPPER_DIR = os.path.dirname(BASE_DIR)
with open(os.path.join(UPPER_DIR, 'keys.json'), 'r') as f:
    json_data = json.load(f)
    token = json_data['slack_token']


channel_name = 'apitest'
# url = 'https://slack.com/api/conversations.list'
url = 'https://slack.com/api/chat.postMessage'
# url = 'https://slack.com/api/apps.permissions.scopes.list'

# my private

headers = {
    # 'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ token
    # 'token':token
}

params = {
    'channel':'C01LMTER118',
    'text':'hello world',
    "attachments": [{
        "text":"Who wins the lifetime supply of chocolate?",
        "fallback":"You could be telling the computer exactly what it can do with a lifetime supply of chocolate.",
        "color":"#3AA3E3","attachment_type":"default",
        "callback_id":"select_simple_1234",
        "actions":[
            {
                "name":"winners_list",
                "text":"Who should win?",
                "type":"select",
                "data_source":"users"
                }
                ]
        }]
}
    # 'token':token


res = requests.post(url, data=json.dumps(params), headers=headers)

print(res.json())
