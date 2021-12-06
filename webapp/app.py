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

#initialize flask
IMAGE_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/')
def index():
    return 'Hello world'

@app.route('/quad')
def quad():
    try:
        cur.execute('''SELECT DeviceID, reading, DataTime
                       FROM devices NATURAL JOIN readings
                       WHERE DataDate >= (CURDATE() - INTERVAL 2 DAY)''')
        records = cur.fetchall()
        
        now = datetime.now()
        data = []
        dates = []
        for record in records:
            dates.append(now - record[2])
            data.append(record[1])
        print(dates, data)
        plt.plot_date(dates, data)
        plt.title('matplotlib.pyplot.plot_date() function Example', fontweight ="bold")
        plt.savefig("static/images/graph.png")
        
    except Exception as ex:
        print("database read error: ")
        print(ex)
    
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graph.png')
    print(filename)
    return render_template('quad.html', graph_image = 'static/images/graph.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

