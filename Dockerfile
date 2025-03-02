FROM python:3.13-slim-bookworm

COPY requirements.txt /app/
COPY src /app/src
COPY tests /app/tests
COPY setup.py /app/
COPY README.md /app/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

