```

```
Установить модуль `virtualenv`
```
~/.local/bin/pip3.10 install virtualenv
```
Cоздать директорию окружения `venv_wselfedu`
```
~/.local/bin/python3.10 -m virtualenv venv_wselfedu
```
Активировать виртуальное окружение
```
source venv_webselfedu/bin/activate
```
Проверяем, что вход выполнен успешно
```
which python
```
=> /home/d/d45400kr/d45400kr.beget.tech/venv_webselfedu/bin/python
```
pip install django==4.2.6
```
Создать одноименный проект в текущей директории `wselfedu .` 
```
django-admin startproject wselfedu .
```
Создать локально `requirements.txt`,по умолчанию без `dev`
```
poetry export -o requirements.txt
```
```
./manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json
```