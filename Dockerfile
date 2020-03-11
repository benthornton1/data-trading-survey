FROM python:3.6-alpine

RUN adduser -D userstudy

WORKDIR /home/userstudy

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN apk update && apk add mariadb-connector-c-dev
RUN apk add jpeg-dev
RUN apk add make automake gcc g++ subversion python3-dev
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations_prod migrations_prod
COPY userstudy.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP userstudy.py

RUN chown -R userstudy:userstudy ./
USER userstudy

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]