FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc libcurl4-openssl-dev libssl-dev

COPY ./dockerfiles/fastapi/api_requirements.txt api_requirements.txt

RUN --mount=type=secret,id=pip.conf,dst=/root/.pip/pip.conf \
    pip install --upgrade pip==22.3 && \
    pip install -r api_requirements.txt

COPY . .

USER 0
RUN apt-get update && apt-get install -y \
    curl \
    nano

EXPOSE 81

RUN chmod +x ./prestart.sh

CMD ["./prestart.sh"]