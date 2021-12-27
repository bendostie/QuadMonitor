# flask web server to serve data from database
# data is graphed with pyplot and served as an image
# Benjamin Dostie 2021

import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
from flask import Flask, render_template

#create database connection
import mysql.connector
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "WebUser",
        password = "Turtle2" )
    cur = conn.cursor()
    cur.execute("USE QuadMonitor")  
except Exception as ex:
    print("database connection error: ")
    print(ex)
    sys.exit("Unrecoverable error")

def get_moisture():
    '''
    get data from moisture sensors in the database,
    graph, and save to image
    '''
    
    try:
        cur.execute('''SELECT DeviceID, reading, DataTime
                       FROM devices NATURAL JOIN readings
                       WHERE DataDate >= (CURDATE() - INTERVAL 2 DAY) AND DeviceType = "soil_moisture"''')
        records = cur.fetchall()
        
        now = datetime.now()
        data = []
        dates = []
        for record in records:
            dates.append(now - record[2])
            data.append(record[1])
        print(dates, data)
        plt.plot_date(dates, data)
        plt.title('Soil Moisture', fontweight ="bold")
        plt.savefig("static/images/moist.png")
        plt.close()
        
    except Exception as ex:
        print("database read error: ")
        print(ex)
        
        
def get_temp():
    '''
    get data from temperature sensors in the database,
    graph, and save to image
    '''
    
    try:
        cur.execute('''SELECT DeviceID, reading, DataTime
                       FROM devices NATURAL JOIN readings
                       WHERE DataDate >= (CURDATE() - INTERVAL 2 DAY) AND DeviceType = "temperature"''')
        records = cur.fetchall()
        
        now = datetime.now()
        data = []
        dates = []
        for record in records:
            dates.append(now - record[2])
            data.append(record[1])
        print(dates, data)
        plt.plot_date(dates, data)
        plt.title('Air Temperature', fontweight ="bold")
        plt.savefig("static/images/temp.png")
        plt.close()
        
    except Exception as ex:
        print("database read error: ")
        print(ex)
        
def get_humidity():
    '''
    get data from humidity sensors in the database,
    graph, and save to image
    '''
    try:
        cur.execute('''SELECT DeviceID, reading, DataTime
                       FROM devices NATURAL JOIN readings
                       WHERE DataDate >= (CURDATE() - INTERVAL 2 DAY) AND DeviceType = "humidity"''')
        records = cur.fetchall()
        
        now = datetime.now()
        data = []
        dates = []
        for record in records:
            dates.append(now - record[2])
            data.append(record[1])
        print(dates, data)
        plt.plot_date(dates, data)
        plt.title('Air Humidity', fontweight ="bold")
        plt.savefig("static/images/humid.png")
        plt.close()
        
    except Exception as ex:
        print("database read error: ")
        print(ex)
        
        
        
#initialize flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quad')
def quad():
    get_moisture()
    get_humidity()
    get_temp()
    return render_template('quad.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

