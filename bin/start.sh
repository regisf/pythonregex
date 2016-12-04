#!/usr/bin/env bash

printf "Starting PythonRegex application in \033[1m"
if [ "$1" = "--dev" ]; then printf "DEVELOPER"; else printf "PRODUCTION"; fi; printf "\033[0m mode\n"

cd Application
python3 main.py $1
