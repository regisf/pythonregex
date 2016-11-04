#!/usr/bin/env bash

printf "Testing project\n"

if [ ! -d "env" ];
then
    printf "No Python virtualenv directory\n"
    exit 1
fi

source env/bin/activate

python tests/test.py

# Quit with the same error code
if [ $? ! 0 ];
then
    exit $?
fi

printf "Done\n"
