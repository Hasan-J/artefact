FROM python:3.10.5-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements /requirements
RUN pip install -r /requirements/local.txt
