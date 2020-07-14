# uwsgi auto start

> emperor mode needed
```bash
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/ssamko/django-pikavue/source/pikavue.ini /etc/uwsgi/vassals/
```

> pikavue.ini
```
...
emperor = /etc/uwsgi/vassals
uid = www-data
gid = www-data
```

