python manage.py migrate
python manage.py create_admin
gunicorn api.wsgi:application -p 8000 & nginx -g "daemon off;"