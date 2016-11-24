#!/bin/sh

USE_DOCKER=0
# Install Python Virtual env only on non docker machine
if [ "$1" != "--docker" ];
then
    # Install virtual env
    printf "Installing python 3 virtual environment\n"
    python3 -m venv env > /dev/null 2>&1
    source env/bin/activate
else
    USE_DOCKER=1
fi

printf "Update pip\n"
pip install --upgrade pip > /dev/null 2>&1

printf "Installing requirements\n"
pip install -r requirements.txt > /dev/null 2>&1

# Use environment variables instead of user entry
# MongoDB should exists
if [ "${USE_DOCKER}" = "0" ];
then
    # First ensure the MongoDB exists and it's reachable, then check the only field required at boot up
    printf "Ensure MongoDB\n"
    IS_CONFIGURED=`mongo pythonregex --quiet --eval "db.configuration.find().length()"`
    if [ $? != 0 ];
    then
        printf "\033[0;31mCan't connect to mongodb. Is it online?\033[0m\n"
        exit 1
    fi

    # The cookie_secret need to be configured before first run
    SECRET=
    if [ "${IS_CONFIGURED}" = "0" ];
    then
        printf "Install new cookie_secret key. You may change it later\n"
        SECRET=`date +%s | shasum -a 256 | base64 | head -c 32`
        mongo pythonregex --quiet --eval "db.configuration.insert({key: 'secret_key', value: '${SECRET}'})"  > /dev/null 2>&1
    else
        printf "The database is already configured\n"
        SECRET=`mongo pythonregex --quiet --eval "db.configuration.find({key: 'secret_key'})[0].value"`
    fi

    # Register admin user
    printf "\nEnter the admin user name: "
    ADMIN_USER=
    while [[ ${ADMIN_USER} = "" ]];
    do
        read ADMIN_USER
    done

    ADMIN_EMAIL=
    printf "Enter your email address (for normal connection): "
    while [[ ${ADMIN_EMAIL} = "" ]];
    do
        read ADMIN_EMAIL
    done

    printf "Enter the admin password:  "
    ADMIN_PASSWORD=
    while [[ ${ADMIN_PASSWORD} = "" ]];
    do
        read ADMIN_PASSWORD
    done
else
    echo "Use docker"
fi

PASSWORD=`python -c "import hashlib;print(hashlib.sha256('${SECRET}'.encode() + '${ADMIN_PASSWORD}'.encode()).hexdigest())"`

NOW=`date +%s`

# Insert all information inside de database
mongo pythonregex --quiet --eval "db.user.insert({
    username: '${ADMIN_USER}',
    email: '${ADMIN_EMAIL}',
    password: '${PASSWORD}',
    creation_date: ${NOW},
    is_admin: true})"

printf "Done\n"
