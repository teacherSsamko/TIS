# gunicorn 실행

>gunicorn.service   
>gunicorn.socket   

파일 작성 후   
```
systemctl enable --now gunicorn.socket
systemctl start gunicorn.service
```
nginx 실행
```
systemctl start nginx
```
시스템 시작시 자동 실행
```
systemctl enable gunicron.service
```
