#!/usr/bin/env bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
done 

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

gunicorn --bind 0.0.0.0:8000 todo_service.wsgi:application