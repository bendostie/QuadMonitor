#script to set up Quad Monitor database for the first time
#Benjamin Dostie, 2021
from datetime import date
from datetime import datetime

import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "SetupUser",
    password = "Turtle2" )

cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS QuadMonitor")
cur.execute("CREATE DATABASE QuadMonitor")
cur.execute("USE QuadMonitor")

cur.execute("DROP TABLE IF EXISTS readings")
cur.execute('''CREATE TABLE devices(
                DeviceID CHAR(3) PRIMARY KEY,
                NodeID VARCHAR(25),
                DeviceType VARCHAR(25))''')
cur.execute('''CREATE TABLE readings(
                DeviceID CHAR(3),
                DataDate DATE,
                DataTime TIME,
                Reading DECIMAL(9, 6),
                
                FOREIGN KEY (DeviceID) 
                REFERENCES devices(DeviceID)
                ON UPDATE CASCADE,
                PRIMARY KEY (DeviceID, DataDate, DataTime))''')
cur.execute('''INSERT INTO devices(DeviceID, NodeID, DeviceType) 
            VALUES ('111', 'Arduino_1', 'soil_moisture')''')

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("'%Y-%m-%d")
cur.execute('''INSERT INTO readings(DeviceID, DataDate, DataTime, Reading) 
            VALUES ('001', %s,%s, 3.14)''', [current_time, current_date])
conn.commit()
conn.close()
