#!/bin/sh
#shell ira encerrar a execução so script quando um comando falhar

set -e
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT ; do
    echo "Waiting for Posrgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 0.1
done
echo "Posrgres Database Startup Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic
python manage.py migrate
python manage.py runserver

