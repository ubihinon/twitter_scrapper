#!/bin/bash

/etc/init.d/nginx start
python3 manage.py migrate
uwsgi --ini /opt/conf/uwsgi.ini
