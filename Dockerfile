FROM python:3.6.6-alpine3.7
RUN apk update && apk add build-base

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "run.py"]