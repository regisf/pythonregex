#!/usr/bin/env bash

. ./bin/tests.sh

cd build
docker build $1 -t pythonregex .
