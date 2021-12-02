#script to set up Quad Monitor database for the first time
#Benjamin Dostie, 2021

import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "SetupUser",
    password = "Turtle2" )

cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS QuadMonitor")
cur.execute("CREATE DATABASE QuadMonitor")
cur.execute("DROP TABLE IF EXISTS SensorData")
cur.execute('''CREATE TABLE PC
                (model CHAR(5) PRIMARY KEY,speed INT, ram INT,hd INT,
                price DECIMAL(7,2) NOT NULL, 
                FOREIGN KEY (model) 
                REFERENCES Product(model)
                ON DELETE CASCADE
                ON UPDATE CASCADE)''')