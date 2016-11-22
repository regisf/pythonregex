#!/usr/bin/env bash

. ./bin/tests.sh

cd build
docker build -t pythonregex:101 .
