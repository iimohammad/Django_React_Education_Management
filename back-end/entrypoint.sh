#! bin/sh 
python3 manage.py migrate --no-input

gunicorn config.wsgi:application bind 0.0.0.0:8000