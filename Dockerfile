FROM python:3.7-slim-stretch

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN apt update && apt install -qy libmariadbclient-dev gcc
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /app

CMD ["sh", "docker-entry.sh"]
