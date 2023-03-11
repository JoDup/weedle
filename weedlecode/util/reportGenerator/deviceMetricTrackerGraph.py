import matplotlib.pyplot as plt
import sqlite3
import os.path

import numpy as np

def createDeviceMetricTrackerGraph(metric,unit):

   # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')

    # Create the graph
    # Execute a SELECT query
    cursor = conn.execute("SELECT best_practice_min, best_practice_max FROM W_DEVICE_METRIC_TRACKER where NAME=? AND best_practice_min is not null",
                   (metric,))

    bpMin = 0
    bpMax = 0
    for row in cursor:
        if bpMin==0:
           bpMin=row[0]
        if bpMax==0:
           bpMax=row[1]
 
    # Execute a SELECT query
    cursor = conn.execute("SELECT hour, value FROM W_DEVICE_METRIC_TRACKER where NAME=? order by w_dmt_id desc",
                   (metric,))
    # Fetch the data
    data = cursor.fetchall()

    # Separate the x and y values
    plt.clf()

    # Generate a random color for the line
    line_color = np.random.rand(3,)

    #x = [row[0] for row in data]
    #x = list(range(1, len(data) + 1))
    x = list(range(0, -len(data), -1))
    y = [row[1] for row in data]
    plt.plot(x, y, color=line_color)

    # add labels and title
    plt.xlabel('Hour')
    plt.ylabel(unit)
    plt.title(metric)
    #print('bpMin '+bpMin)
    #print('bpMax '+bpMax)
    
    plt.axhline(y=float(bpMin), color='r', linestyle='--')
    plt.axhline(y=float(bpMax), color='r', linestyle='--')

    
    filename = metric + '.png'
    filepath = '/home/weedle/weedlecode/weedleReport/' + filename

    # Check if file already exists
    if os.path.isfile(filepath):
       os.remove(filepath)
    # display plot
    #plt.show()
    # Save the graph as a PNG file
    plt.savefig(filepath)

