FROM alpine

MAINTAINER Regis FLORET

LABEL com.python-regex.version="1.0.1"

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

COPY requirement.txt /tmp
RUN pip3 install -r /tmp/requirement.txt

RUN git clone