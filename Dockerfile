FROM python:alpine

MAINTAINER Regis FLORET <regisfloret@gmail.com>

LABEL com.python-regex.version="1.0.1"

# Change for the project

WORKDIR pythonregex

COPY requirements.txt requirements.txt
COPY Application Application
COPY bin bin

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["bin/start.sh"]
