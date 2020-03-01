flask db upgrade
gunicorn -b 0.0.0.0:80 -w 2 app:app