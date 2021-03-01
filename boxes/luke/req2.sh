#!/bin/bash
token=$(curl -X POST -H 'Content-Type: application/json' -d '{"username":"admin", "password":"Zk6heYCyv6ZE9Xcg"}' http://10.10.10.137:3000/login 2>/dev/null | awk -F "\"" {'print $10'})
curl -X POST -d "{\"username\":\"$1\", \"password\":\"$2\"}" http://10.10.10.137/management/
