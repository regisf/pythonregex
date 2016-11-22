FROM ubuntu

MAINTAINER Regis FLORET <regisfloret@gmail.com>

LABEL com.python-regex.version="1.0.1"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install apt-utils python3 python3-pip  git mongodb -y && \
    \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    \
    service mongodb start && \
    \
    git clone -b add-docker https://github.com/regisf/pythonregex.git && \
    cd pythonregex && \
    bin/install.sh --docker && \
    \
    apt-get autoremove -y && \
    apt-get clean

EXPOSE 8888
WORKDIR pythonregex
CMD bin/run.sh
