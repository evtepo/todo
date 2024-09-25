FROM python:3.11-slim

WORKDIR /src

COPY docker/launch.sh launch.sh
COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install netcat-traditional \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "launch.sh"]