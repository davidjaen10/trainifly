#!/bin/sh
export DJANGO_SETTINGS_MODULE=trainifly.settings
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
