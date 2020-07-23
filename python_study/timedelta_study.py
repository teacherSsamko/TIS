import datetime

today = datetime.date.today()
# datetime.date.resolution. 
# 같지 않은 date 객체 간의 가능한 가장 작은 차이, timedelta(days=1)
yesterday = datetime.date.today() - datetime.date.resolution
print(type(yesterday))
print(yesterday)

now = datetime.datetime.now()
# datetieme.date()
# datetime 객체를 date객체로 변환시켜줌.
if now.date() > yesterday:
    print(now.date())
    print('now is more important')