FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . /app/

COPY .env.docker /app/.env

ENV APP_NAME=NAILS

EXPOSE 8000
CMD gunicorn nails.wsgi:application -b 0.0.0.0:8000
