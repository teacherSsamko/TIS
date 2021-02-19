import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR,'video_list.txt'), 'r') as f:
    ids = f.readlines()

url_prefix = 'https://www.youtube.com/watch?v='
with open(os.path.join(BASE_DIR,'video_url_list.txt'), 'w') as f:
    for id in ids:
        f.write(f'{url_prefix}{id}')