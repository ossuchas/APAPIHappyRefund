#!/bin/bash
if [ -z "$1" ]; then
    echo 'You must specify a Docker Hub username!'
    exit 1
else
    fullname=$1
fi

docker-compose build

docker push ${fullname}
