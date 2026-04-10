web: gunicorn cryptovest.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
release: python manage.py migrate --run-syncdb && python manage.py create_superuser && python manage.py collectstatic --noinput
