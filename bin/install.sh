#!/usr/bin/env bash

# Install Python Virtual env only on non docker machine
if [ "$1" != "--docker" ];
then
    # Install virtual env
    printf "Installing python 3 virtual environment\n"
    python3 -m venv env > /dev/null 2>&1
    source env/bin/activate
fi

printf "Update pip\n"
pip install --upgrade pip > /dev/null 2>&1

printf "Installing requirements\n"
pip install -r requirements.txt > /dev/null 2>&1

printf "Ensure MongoDB\n"
IS_CONFIGURED=`mongo pythonregex --quiet --eval "db.configuration.find().length()" > /dev/null 2>&1`
if [ $? != 0 ];
then
    printf "\033[0;31mCan't connect to mongodb. Is it online?\033[0m\n"
    exit 1
fi

if [ "$IS_CONFIGURED" = "0" ];
then
    SECRET=`date +%s | shasum -a 256 | base64 | head -c 32`
    echo ${SECRET}
fi

printf "Done\n"

