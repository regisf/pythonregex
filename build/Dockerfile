FROM alpine

MAINTAINER Regis FLORET

LABEL com.python-regex.version="1.0.1"

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    apk add --no-cache git&& \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    git clone https://github.com/regisf/pythonregex.git && \
    cd pythonregex && \
    bin/install.sh --docker

EXPOSE 3000
WORKDIR pythonregex
CMD bin/run.sh
