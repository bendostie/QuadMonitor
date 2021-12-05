
import socket
import threading
from datetime import datetime
ip_address = "0.0.0.0"
port = 2001

import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "SetupUser",
    password = "Turtle2" )
cur = conn.cursor()
cur.execute("USE QuadMonitor")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_address, port))
server.listen()
try:
    while True:
        print("Waiting for connection")
        connection, client = server.accept()
     
        try:
            print("Connected to client IP: {}".format(client))
             
            # Receive and print data 32 bytes at a time, as long as the client is sending something
            while True:
                data = connection.recv(32)
                print("Received data: {}".format(data))
                
                try:
                    id_code= data[0:3]
                    reading = float(data[3:])
                    print("data")
                    print(id_code)
                    print(reading)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    current_date = now.strftime("%Y-%m-%d")
                    cur.execute('''INSERT INTO readings(DeviceID, DataDate, DataTime, Reading) 
                VALUES (%s, %s,%s, %s)''', [id_code, current_date, current_time, reading])
                    conn.commit()
                except Exception as ex:
                    print("invalid data")
                    print(ex)
                    break
                if not data:
                    break
     
        finally:
            connection.close()
except KeyboardInterrupt:
    server.close()
    conn.commit()
    conn.close()