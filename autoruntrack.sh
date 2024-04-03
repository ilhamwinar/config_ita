#!/bin/bash
#!/usr/bin/env python3

export DISPLAY=:0 #needed if you are running a simple gui app.

cd "$(dirname "$0")"

process=AICCTV
while true
do
    if ! ps aux | grep -v grep | grep 'python3 sender.py' > /dev/null
    then
        python3 sender.py &
        sleep 5
    fi
done
exit
