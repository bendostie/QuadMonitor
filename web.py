import matplotlib.pyplot as plt
from datetime import datetime


import mysql.connector
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "WebUser",
        password = "Turtle2" )
    cur = conn.cursor()
    cur.execute("USE QuadMonitor")
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
    plt.savefig("Graph.png")
    plt.show()
except Exception as ex:
    print("database error: ")
    print(ex)
