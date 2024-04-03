#!/bin/bash
#!/usr/bin/env python3



cd "$(dirname "$0")"
process=api_forecasting_service_prola
while true
do
    if ! ps aux | grep -v grep | grep 'python3 api_add_cctv.py' > /dev/null
    then #{}
        python3 api_add_cctv.py &
        sleep 5 #{}
    fi #{}


sleep 10
done
exit