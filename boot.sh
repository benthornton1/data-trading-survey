#!/bin/sh
source venv/bin/activate
while true; do
    flask db migrate --directory=migrations_prod
    flask db upgrade --directory=migrations_prod
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - userstudy:app