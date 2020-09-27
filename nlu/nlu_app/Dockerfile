FROM python:3.7.7-slim-stretch

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        mecab \
        libmecab-dev \
        unidic-mecab \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip3 install pip --upgrade && \
    pip3 install Flask==1.1.1 camphr==0.5.9 mecab-python3==0.996.5 \
                 Cython==0.29.16 spacy==2.2.4 hydra-colorlog==0.1.4 hydra-core==0.11.3
RUN pip3 install fugashi==0.1.9

WORKDIR /app