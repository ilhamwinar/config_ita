

#!/bin/bash
#!/usr/bin/env 

export DISPLAY=:0 #needed if you are running a simple gui app.

cd "$(dirname "$0")"
sleep 15
process=script_ntp
while true
do

    if ! ps aux | grep -v grep | grep 'python3 ITA.py --Location JAPEK KM47 200' > /dev/null
    then 
        python3 ITA.py --Location 'JAPEK KM47 200' &
        sleep 15 
    fi 
sleep 10
done
exit
        