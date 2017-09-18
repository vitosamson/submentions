FROM python:alpine

RUN pip install praw

COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "app.py"]
