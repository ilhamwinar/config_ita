import os
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import time


cwd = os.getcwd()
def write_log(lokasi_log, datalog):
    waktulog = datetime.now()
    dirpathlog = f"Log/{lokasi_log}"
    os.makedirs(dirpathlog, exist_ok=True)
    pathlog = f"{waktulog.strftime('%d%m%Y')}.log"
    file_path = Path(f"{dirpathlog}/{pathlog}")
    datalog = "[INFO] - " + datalog
    if not file_path.is_file():
        file_path.write_text(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
    else :
        fb = open(f"{dirpathlog}/{pathlog}", "a")
        fb.write(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
        fb.close
    
    print(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}")

if __name__ == '__main__':
    #KILL ALL MYSCRIPT

    while True:
        time.sleep(15)
        try:
            x = subprocess.check_output([ 'pgrep',  '-f',  cwd+"/myscript.sh"])
            out = x.decode("utf-8").split()[0]
            #print("API", "VIA CWD "+out)
            write_log("API", "MASIH ADA MYSCRIPT VIA CWD "+out)
            #os.system("kill "+out)
            time.sleep(5)

        except:
            try:
                x = subprocess.check_output([ 'pgrep',  '-f', "/myscript.sh"])
                print(x)
                out = x.decode("utf-8").split()[0]
                # print("YANG TIDAK ADA CWD")
                # print(out)
                #print("API", "TIDAK VIA CWD "+out)
                write_log("API", "MASIH ADA MYSCRIPT TIDAK VIA CWD "+out)
                #os.system("kill "+out)
                time.sleep(5)
                
            except:
                #print("tidak ada")
                write_log("API", "TIDAK ADA MYSCRIPT YANG JALAN")
                #time.sleep(3)
                os.system("chmod +x "+cwd+"/myscript.sh;")
                os.system("./myscript.sh &")
                os.system("killall python3")
                pass
            pass