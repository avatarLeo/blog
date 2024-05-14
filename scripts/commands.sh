#!/bin/sh
#shell ira encerrar a execução so script quando um comando falhar

set -e
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT ; do
    echo "Waiting for Posrgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 2
done
echo "Posrgres Database Startup Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations  --noinput
python manage.py migrate  --noinput
python manage.py runserver 0.0.0.0:8000

