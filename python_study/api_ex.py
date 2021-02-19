import sys

import requests


def main(word):
    print('hello', word)
    print(f'{word}\n'*5)
    sample_url = 'http://35.192.129.163:5000/rec_prod?prod=%EC%8B%A0%EC%9D%BC%20%EB%8D%94%EC%8E%88%EC%BF%A8%20%EB%83%89%ED%92%8D%EA%B8%B0%20SIF-D27MD%20%EC%B4%88%ED%8A%B9%EA%B0%80'
    url = 'http://35.192.129.163:5000/rec_prod'
    params = {'prod':'[디디에벨라] 14k 스왈로브스키 8mm 진주 귀걸이'}
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.text)


img_url = sys.argv[-1]
main(img_url)