#!/bin/bash
#!/usr/bin/env python3

cd "$(dirname "$0")"
process=api_forecasting_service_prola
while true
do

    if ! ps aux | grep -v grep | grep 'python3 stop.py' > /dev/null
    then #{}
        python3 stop.py &
        sleep 3 #{}
    fi #{}

sleep 10
done
exit