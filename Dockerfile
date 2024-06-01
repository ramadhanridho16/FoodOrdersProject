FROM python:3.12.3-slim
LABEL authors="Pinara"

WORKDIR /app

RUN apt-get update -y

RUN apt-get upgrade -y

RUN apt-get install libpq-dev -y gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN bash -c 'mkdir -pv /app/static/images && cd /app/static/images && mkdir menus && mkdir banners'

ENV PYTHONBUFFERED=1
ENV SECRET_KEY="rahasiagessecret"
ENV DB_USERNAME="root"
ENV DB_PASSWORD=""
ENV DB_HOST="localhost"
ENV MAX_FILE_SIZE=5242880
ENV APP_PORT=8000

EXPOSE ${APP_PORT}/tcp

CMD python manage.py runserver 0.0.0.0:${APP_PORT}