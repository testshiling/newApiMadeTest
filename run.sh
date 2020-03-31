#!/bin/bash
pwd

mkdir -p /root/.pip/
cp pip.conf /root/.pip/pip.conf
pip install -r /usr/src/app/requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000  --insecure
