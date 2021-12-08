import matplotlib.pyplot as plt
import os
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

def get_moisture():
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
IMAGE_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/')
def index():
    return 'Hello world'

@app.route('/quad')
def quad():
    get_moisture()
    get_humidity()
    get_temp()
    return render_template\
           ('quad.html', moist_image = 'static/images/moist.png', \
            temp_image = 'static/images/temp.png', humid_image = 'static/images/humid.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

