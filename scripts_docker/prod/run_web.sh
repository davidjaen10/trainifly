#!/bin/sh

echo "Esperando a Postgres..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

echo "Postgres listo, aplicando migraciones..."

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn --chdir /code/trainifly --bind 0.0.0.0:8000 trainifly.wsgi:application
