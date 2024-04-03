import os
import requests
import logging
import mysql.connector
import socket
import subprocess
from pathlib import Path
from datetime import datetime

delay=20

user="dbdev"
password="jmto2024"
host="175.10.1.101"
database="db_aicctv"
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

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to a remote server (doesn't actually send data)
        s.connect(('8.8.8.8', 80))
        
        # Get the local IP address from the socket
        local_ip_address = s.getsockname()[0]
        
        return local_ip_address
    except Exception as e:
        # Handle errors
        print("Error:", e)
        return None
    finally:
        # Close the socket
        s.close()

def make_word(script_path,script_content):
    with open("myscript.sh", "w") as script_path:
        script_path.write(script_content)

def add_newline(script_path,line_to_add):
    try:
        with open(script_path, "a") as script_file:
            script_file.write("\n" + line_to_add)
        print(f"Line has been successfully added to '{script_path}'.")
    except FileNotFoundError:
        print(f"Script '{script_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_word(script_path,word_to_remove):
    try:
        with open(script_path, "r") as script_file:
            lines = script_file.readlines()

        # Remove lines containing the specified text
        modified_lines = [line.replace(word_to_remove, "") for line in lines]

        with open(script_path, "w") as script_file:
            script_file.writelines(modified_lines)

        print(f"Text '{word_to_remove}' has been successfully removed from '{script_path}'.")
    except FileNotFoundError:
        print(f"Script '{script_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_lines_and_following(file_path, target_word, lines_to_delete=5):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find lines containing the target word and delete them along with the following lines
    modified_lines = []
    skip_next_lines = 0
    for line in lines:
        if target_word in line:
            # Skip this line and the following lines_to_delete lines
            skip_next_lines = lines_to_delete
        elif skip_next_lines > 0:
            # Skip this line
            skip_next_lines -= 1
        else:
            modified_lines.append(line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Lines containing '{target_word}' and the next {lines_to_delete} lines deleted successfully.")

if __name__ == '__main__':

    #KILL ALL MYSCRIPT

    try:
        x = subprocess.check_output([ 'pgrep',  '-f',  cwd+"/myscript.sh"])
        out = x.decode("utf-8").split()[0]
        write_log("API", "VIA CWD "+out)
        os.system("kill "+out)

    except:
        try:
            x = subprocess.check_output([ 'pgrep',  '-f', "/myscript.sh"])
            out = x.decode("utf-8").split()[0]
            # print("YANG TIDAK ADA CWD")
            # print(out)
            write_log("API", "TIDAK VIA CWD "+out)
            os.system("kill "+out)
            
        except:
            pass
        pass

    ## Inisialisasi mysql
    try:
        x = subprocess.check_output([ 'pgrep',  '-f',  "python3 ITA.py --Location "])
        out = x.decode("utf-8").split()[0]
        os.system("kill "+out)
        write_log("API", "BERHASIL KILL ALL LOCATION")

    except:
        write_log("API", "TIDAK ADA TITIK")
        pass
        
    try:
        cnx=mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        if cnx.is_connected():
            logging.info("DATABASE CONNECTED TO CU_Config_V2")

    except:
        logging.info("DATABASE NOT CONNEDTED TO CU_Config_V2")


    # Execute a SELECT query
    local_ip = get_local_ip()
    query = "select location from CU_Config_V2 where address = '"+str(local_ip)+"' "+"and status_button = '1'"
    cursor = cnx.cursor()
    cursor.execute(query)

    # Fetch all the rows as a list of tuples
    rows = cursor.fetchall()

    if rows == []:
        #print("tidak ada")
        write_log("API", "TIDAK ADA YANG BERSTATUS 1, PROGRAM EXIT")
        exit()

    ## Make file and create header
    try:
        os.remove("./myscript.sh")
    except:
        pass
    os.system("touch myscript.sh")
    header_script = """
#!/bin/bash
#!/usr/bin/env 

export DISPLAY=:0 #needed if you are running a simple gui app.

cd "$(dirname "$0")"
sleep 15
process=script_ntp
while true
do"""    
    add_newline("myscript.sh",header_script)


    temp_titik=[]
    for row in rows:

        delete_word("myscript.sh","sleep 10")
        delete_word("myscript.sh","done")
        delete_word("myscript.sh","exit")

        script_content = """
    if ! ps aux | grep -v grep | grep 'python3 ITA.py --Location {}' > /dev/null
    then 
        python3 ITA.py --Location '{}' &
        sleep 15 
    fi 
sleep 10
done
exit
        """.format(row[0],row[0])
        add_newline("myscript.sh",script_content)

        write_log("API", "YANG DITULIS ADALAH TITIK "+row[0])

    #time.sleep(60)
            
    os.system("chmod +x "+cwd+"/myscript.sh;")
    write_log("API", "BERHASIL CHMOD +X")


    os.system("./myscript.sh &")
    write_log("API", "MENJALANKAN MYSCRIPT")

    # # Close the cursor and connection
    cursor.close()
    cnx.close()
    write_log("API", "SUDAH SELESAI WRITE CODE BARU ITA, PROGRAM SELESAI")





