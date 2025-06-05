FROM debian:12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libmariadb-dev gcc pkg-config \
    && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
COPY activeut /app/
COPY aut /app/
COPY manage.py /app/

RUN pip3 install --break-system-packages --upgrade pip && pip3 install --break-system-packages -r requirements.txt

COPY . /app

