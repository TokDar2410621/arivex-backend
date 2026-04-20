web: gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 3 --access-logfile - --error-logfile -
release: python manage.py migrate --noinput
