#!/bin/sh

. ./bin/tests.sh

docker build $1 -t pythonregex/web .
