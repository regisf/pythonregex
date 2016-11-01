#!/usr/bin/env bash

# Install Python Virtual env only on non docker machine
if [ "$1" != "--docker" ]; then
    # Install virtual env
    printf "Installing python 3 virtual environment\n"
    python3 -m venv env > /dev/null 2>&1
    source env/bin/activate
fi

printf "Update pip\n"
pip install --upgrade pip > /dev/null 2>&1

printf "Installing requirements\n"
pip install -r requirements.txt > /dev/null 2>&1

printf "Done\n"

