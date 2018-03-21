FROM python:alpine

RUN pip3 install praw

COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "app.py"]
