FROM python:3.11-slim

WORKDIR /src


COPY requirements.txt requirements.txt
COPY docker/launch.sh launch.sh

RUN apt-get update \
    && apt-get -y install netcat-traditional \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "launch.sh"]