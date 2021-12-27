# this file waits for the sensor node to connect 
# and inserts  reading into database
# Benjamin Dostie, 2021

import socket
import sys
import threading
from datetime import datetime
import mysql.connector

ip_address = "0.0.0.0"
port = 2001

# connect to database
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "ServerUser",
        password = "Turtle2" )
    cur = conn.cursor()
    cur.execute("USE QuadMonitor")
except Exception as ex:
    print("Error opening database: ")
    print(ex)
    sys.exit("Unrecoverable error")

# start server
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, port))
    server.listen()
except Exception as ex:
    print("Error starting server: ")
    print(ex)
    sys.exit("Unrecoverable error")

# wait for conection and insert data
while True:
    try:
        print("Waiting for connection")
        connection, client = server.accept()  
        print("Connected to client IP: {}".format(client))
         
        # after connection recieve data 32 bytes at a time
        # data is formatted as 3 character sensor ID 
        # followed by sensor reading
        while True:
            data = connection.recv(32)
            print("Received data: {}".format(data))
            try:
                id = data[0:4]
                reading = float(data[4:])
                
                # add date and time to data
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_date = now.strftime("'%Y-%m-%d")
                cur.execute('''INSERT INTO readings(DeviceID, 
                            DataDate, DataTime, Reading) 
                            VALUES ('001', %s,%s, 3.14)''', 
                            [current_time, current_date])
            except:
                print("invalid data")
            if not data:
                break
 
    finally:
        connection.close()
        