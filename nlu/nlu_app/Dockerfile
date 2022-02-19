FROM python:3.8.12-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        libmecab-dev \
        build-essential \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip3 install pip --upgrade && \
    pip3 install Flask==1.1.4 camphr==0.5.23 mecab-python3==1.0.5 Cython==0.29.28 \
                 spacy==2.2.4 fugashi[unidic]==1.1.2 markupsafe==2.0.1 && \
    python3 -m unidic download

WORKDIR /app