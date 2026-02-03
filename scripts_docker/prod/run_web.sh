#!/bin/sh
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn --chdir /code/trainifly --bind 0.0.0.0:8000 trainifly.wsgi:application
