import requests

test_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoicmFuaSIsImlhdCI6MTU5MzY4NDg0MH0.1qsC29OCoTYyp459nbSu9bnpkFWR7-m3kIrc_q0gP54'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoib25lbW9tZW50IiwiaWF0IjoxNTk2NDE5ODA0fQ.ixwcb7tCEAw4af6AGzpvSVJUzd2jgTAh_hc3Qn_N8Vs'

headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
            # 'x-access-token': test_token



func = getattr(requests, 'get'.lower())
func2 = getattr(requests, 'post'.lower())

def check_api(bookId):
    # url = 'http://dev-partner.baroquick.kr/api/corps/rani/deliveries/{}'.format(bookId)
    url = 'http://partner.baroquick.kr/api/corps/onemoment/deliveries/{}'.format(bookId)
    res = func(url, json=None, headers=headers)
    if res.ok:
        try: 
            print('reuslt:',res.text)
        except UnicodeEncodeError:
            pass

        result = res.json()
        print()
        print(result['pickupDateScheduled'])
        print(type(result['pickupDateScheduled']))
    else:
        print(res)
        print('fail')

# check_api(1080550308)

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoib25lbW9tZW50IiwiaWF0IjoxNTk2NDE5ODA0fQ.ixwcb7tCEAw4af6AGzpvSVJUzd2jgTAh_hc3Qn_N8Vs'

headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
func2 = getattr(requests, 'post'.lower())

data = {
	"spotCode": "10147",
	"receiverName": "TEST",
	"receiverMobile" :"01012341234",
	"receiverAddress" : "서울특별시 강남구 삼성동 111-11 (삼성동 동남빌딩)",
	"receiverAddressDetail" : "3 층12314qqq",
	"productName": "TEST 커피12314qqq",
	"memoFromCustomer": "TEST123124qqq",
	"productPrice": "15000",
	"corpNumber" : "",
	"orderIdFromCorp" : ""
}

def delivery_api():
    url = 'https://partner.baroquick.kr/api/corps/onemoment/deliveries/'
    res = func2(url, json=data, headers=headers)
    print(res)
    if res.ok:
        try: 
            print('reuslt:',res.text)
        except UnicodeEncodeError:
            pass

        result = res.json()

        print(result)
    

delivery_api()