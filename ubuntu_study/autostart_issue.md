# (재)부팅시 가상환경 설정하는 법
startup 대신 systemd를 사용

## 위치
/etc/systemd/system/{{service}}.service

## 파일 구성
[Unit]

Description=gunicorn daemon

After=network.target

[Service]

User=myuser

Environment="TEST_ENV=production"

WorkingDirectory=/home/myuser/myapp

ExecStart=/usr/bin/python /home/depp/ff_server/app.py

Restart=always

[Install]

WantedBy=multi-user.target

## 실행 cmd
systemctl daemon-reload
systemctl start {name}.service

