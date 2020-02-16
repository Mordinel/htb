#!/bin/bash

if [ "$2" == "" ];
then
    printf "Usage:\n\t$0 [request-type] [api-endpoint]\ne.g:\n\t$0 GET auth/check\n";
    exit
fi

HTTP_TYPE=$(echo -n "$1" | tr '[:lower:]' '[:upper:]')
ENDPOINT=$2

TOKEN=$(curl -k -X GET -H "Content-Type: application/json" -H "Authorization: Basic ZGluZXNoOjRhVWgwQThQYlZKeGdk" https://api.craft.htb/api/auth/login 2>/dev/null | awk -F "\"" {'print $4'})

RESPONSE=$(curl -k -X GET -H "Content-Type: application/json" -H "X-Craft-Api-Token: $TOKEN" https://api.craft.htb/api/auth/check 2>/dev/null | awk -F "\"" {'print $4'})

if [ "$RESPONSE" != 'Token is valid!' ];
then
    echo "$RESPONSE";
    exit;
fi

curl -k -X "$HTTP_TYPE" -H "accept: application/json" -H "X-Craft-Api-Token: $TOKEN" "https://api.craft.htb/api/$ENDPOINT"
