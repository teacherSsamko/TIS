# column type 변경

## int to string(varchar)
ffmpeg이 29.97같은 frame rate를 30000/1001 이런식으로 return해서
기존에 Int였던 column을 string으로 변경해야 하는 상황.

기존에 저장된 int값들을 string으로 변환 후 처리해줘야 할까 싶었는데

models.py에서 
fps = models.IntegerField() 를
fps = models.CharField(max_length=15, null=True) 로 변경해주니 끝.

자동으로 int를 string으로 변환해준다. 

아마 반대의 경우라면 문제가 발생했을 듯.