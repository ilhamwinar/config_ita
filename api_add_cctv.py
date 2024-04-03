from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
import logging
import sys
from datetime import datetime
import mysql.connector
import socket

user="ita_db"
password="Jmt02024!#db"
host="175.10.1.11"
database="db_aicctv"

# user="dbdev"
# password="jmto2024"
# host="175.10.1.101"
# database="db_aicctv"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

#inisialisasi logging
file_handler = logging.FileHandler(filename="./log_server_api.log")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=handlers,
    datefmt="%m/%d/%Y %H:%M:%S",
)
logger = logging.getLogger('LOGGER_NAME')

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


def used_ita(ip):
    logging.info("START TO UPDATE START SERVICE ITA WITH CHANGING BUTTON")
    logging.info(ip)

    #global cnx
    global user
    global password
    global host
    global database

    logging.info(user)
    try:
        cnx=mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
    except:
        logging.info("DATABASE NOT CONNECTED TO GET DATA")
        raise HTTPException(status_code=400, detail="Not Connected Database")

    if cnx.is_connected():
        logging.info("DATABASE CONNECTED TO GET DATA")

    sql ="select status_button from CU_Config_V2 WHERE address = '"+ip+"'"
    print(sql)
    
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        result_query = cursor.fetchall()
    except:
        logging.info("ERROR QUERY GET MASTER_CCTV ADDRESS")
        raise HTTPException(status_code=500, detail="ERROR QUERY GET MASTER CCTV ADDRESS")

    logging.info(result_query)
    temp_result=[]

    for i in result_query:
        print(i[0])
        if i[0] == 1:  
            temp_result.append(i[0])
         
    #print(temp_result)
    total_used_ita=len(temp_result)
    cursor.close() 
    cnx.close()  
    return total_used_ita

def update_master_server(used_cam,ip):

        #global cnx
        global user
        global password
        global host
        global database
        
        logging.info(user)

        sql= """UPDATE master_server
                SET used_cam = %s
                WHERE address = %s
            """
        #UPDATE CU_Config_V2 SET status_button = 1 WHERE id = 50
        logging.info(sql)
        #sql=""" INSERT INTO master_server (address,nama_server,lokasi_server,type,used_cam,capacity_cam) VALUES (%s,%s,%s,%s,%s,%s) """

        try:
            cnx=mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=database
            )
        except:
            logging.info("DATABASE NOT CONNECTED TO GET DATA")
            raise HTTPException(status_code=400, detail="Not Connected Database")

        if cnx.is_connected():
            logging.info("DATABASE CONNECTED TO GET DATA")

        try:

            params = [used_cam,ip]
            cursor = cnx.cursor()
            cursor.execute(sql,params)
            cnx.commit()

        except:
            logging.info("ERROR INSERT or UPDATE master CCTV ")
            raise HTTPException(status_code=500, detail="ERROR INSERT or master CCTV ")
            
        status="BERHASIL CHANGING DATA USED CAM"
        status_id=1
        logging.info("BERHASIL UPDATE DATA")
        cursor.close() 
        cnx.close()  
        return status,status_id


@app.get("/reboot")
async def reboot_pc():
    os.system("reboot")
    return {"message": "berhasil perintah restart service cctv"}



@app.get("/start_cctv")
async def create_cctv():
    local_ip = get_local_ip()
    ip=str(local_ip)
    try:
        os.system("python3 start_list.py &")
        status_id=1
    except:
        status_id=0
    
    total_used_cam=used_ita(ip)
    status,status_id=update_master_server(total_used_cam,ip)

    return {"status": status, "status_id":status_id, "ip_server":ip }

@app.get("/stop_cctv")
async def stop_cctv():
    local_ip = get_local_ip()
    ip=str(local_ip)
    try:
        os.system("python3 stop_list.py")
        status_id=1
    except:
        status_id=0
    
    

    # os.system("chmod +x "+cwd+"/myscript.sh;")
    # os.system("./myscript.sh &")

    total_used_cam=used_ita(ip)
    status,status_id=update_master_server(total_used_cam,ip)

    return {"status": status, "status_id":status_id, "ip_server":ip }

if __name__ == "__main__":
    uvicorn.run("api_add_cctv:app",host="0.0.0.0",port=8400,reload=True)