FROM python:3.6

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "run.py"]