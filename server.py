import socket
import threading
from datetime import datetime
ip_address = "10.65.1.234"
port = 81

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
                id = data[0:4]
                reading = float(data[4:])
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_date = now.strftime("'%Y-%m-%d")
                cur.execute('''INSERT INTO readings(DeviceID, DataDate, DataTime, Reading) 
            VALUES ('001', %s,%s, 3.14)''', [current_time, current_date])
            except:
                print("invalid data")
            if not data:
                break
 
    finally:
        connection.close()