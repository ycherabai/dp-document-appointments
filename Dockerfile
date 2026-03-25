FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -q && \
    apt-get install -y -q python3.11 python3.11-distutils wget curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 && \
    python3.11 -m pip install seleniumbase && \
    python3.11 -m seleniumbase install chromedriver

WORKDIR /app
COPY requirements.txt check_queue.py ./

CMD python3.11 check_queue.py
