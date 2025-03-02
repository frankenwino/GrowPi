FROM python:3.11-slim-bookworm

# COPY requirements.txt /app/
# COPY src /app/src
# COPY tests /app/tests
# COPY setup.py /app/
# COPY README.md /app/

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    python3-pip \
    libgpiod2 \
    python3-libgpiod \
    python3-pigpio \
    && apt-get clean \
    && apt-get autoremove -y\
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

