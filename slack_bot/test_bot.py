import os
import json
import requests


from slacker import Slacker
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPPER_DIR = os.path.dirname(BASE_DIR)
with open(os.path.join(UPPER_DIR, 'keys.json'), 'r') as f:
    json_data = json.load(f)
    token = json_data['slack_token']


channel_name = 'apitest'
url = 'https://slack.com/api/conversations.list'

params = {
    'Content-Type': 'application/x-www-form-rulencoded',
    'token':token
}

print(token)
slack = Slacker(token)
slack.chat.post_message('#apitest', 'hello')

# res = requests.get(url, params=params)

# print(res.json())
# channel_list = json.JSONDecoder(res.json()['channels'])
# print(channel_list)


# client = WebClient(token=os.environ[token])

# try:
#     response = client.chat_postMessage(channel='#apitest', text="Hello world!")
#     assert response["message"]["text"] == "Hello world!"
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")