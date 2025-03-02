FROM python:3.13-slim-bookworm

# COPY requirements.txt /app/
# COPY src /app/src
# COPY tests /app/tests
# COPY setup.py /app/
# COPY README.md /app/

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libgpiod2 \
    && apt-get clean \
    && apt-get autoremove -y\
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

