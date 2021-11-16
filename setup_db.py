#script to set up Quad Monitor database for the first time
#Benjamin Dostie, 2021

import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "SetupUser",
    password = "Turtle2" )

cur = conn.cursor()
cur.execute("CREATE DATABASE QuadMonitor")
cur.execute('''CREATE TABLE Product
                (maker CHAR(2), model CHAR(5), type VARCHAR(8), PRIMARY KEY (maker, model) )''')