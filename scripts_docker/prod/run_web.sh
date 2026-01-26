#!/bin/sh
su -m django_user -c "python manage.py migrate"

su -m django_user -c "python manage.py collectstatic --noinput"

chmod -R 755 /code/staticfiles

exec su -m django_user -c "gunicorn --chdir /code/trainifly --bind 0.0.0.0:8000 trainifly.wsgi:application"

