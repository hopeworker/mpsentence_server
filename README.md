# mpsentence_server

## code prepare
1. git clone https://github.com/hopeworker/mpsentence_server.git
2. rename "mpsentence_s/mpsentence_s/your_local_settings.js" to "mpsentence_s/mpsentence_s/settings.js", and edit this file with your personal settings.

## setup virtual env
```bash
$pip install virtualenv
$cd myproject/
$virtualenv --no-site-packages venv
$source venv/bin/activate
(venv)pip install -r requirements.txt

```
## run server
```bash
(venv)$ cd mpsentence_s
(venv)mpsentence_s$ python manage.py runserver 192.168.0.25:8000

```



