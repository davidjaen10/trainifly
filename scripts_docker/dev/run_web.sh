#!/bin/sh
su -m django_user -c "python manage.py runserver 0.0.0.0:8000"
su -m django_user -c "python manage.py makemigrations"
su -m django_user -c "python manage.py migrate"