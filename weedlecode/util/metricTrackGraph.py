import smtplib
import matplotlib.pyplot as plt
import sqlite3
import os.path
import numpy as np

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def createTrackerGraph(metric,unit):

   # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')

    # Create the graph
    # Execute a SELECT query
    cursor = conn.execute("SELECT best_practice_min, best_practice_max FROM W_METRIC_TRACKER where NAME=? AND best_practice_min is not null",
                   (metric,))

    bpMin = 0
    bpMax = 0
    for row in cursor:
        if bpMin==0:
           bpMin=row[0]
        if bpMax==0:
           bpMax=row[1]
 
    # Execute a SELECT query
    cursor = conn.execute("SELECT hour, value FROM W_METRIC_TRACKER where NAME=? order by w_mt_id desc",
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
    filepath = '/home/weedle/weedlecode/trackerGraph/' + filename

    # Check if file already exists
    if os.path.isfile(filepath):
       os.remove(filepath)
    # display plot
    #plt.show()
    # Save the graph as a PNG file
    plt.savefig(filepath)

def sendMail():
    # Set up the email
    msg = MIMEMultipart()

    msg['From'] = 'climate@gmail.com'
    msg['To'] = 'joel.dupont@gmail.com'
    msg['Subject'] = 'Weedle Capture'

    # Define the file paths of the images
    file_paths = ['/home/weedle/weedlecode/trackerGraph/Temperature.png',
                  '/home/weedle/weedlecode/trackerGraph/Soil-Moisture.png',
                  '/home/weedle/weedlecode/trackerGraph/Soil-Fertility.png', 
                  '/home/weedle/weedlecode/trackerGraph/Sun.png']

    # Attach each file to the email
    for file_path in file_paths:
       if os.path.isfile(file_path):
          with open(file_path, 'rb') as f:
              img = MIMEImage(f.read())
              msg.attach(img)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
       smtp.starttls()
       smtp.login('weedlepilot@gmail.com', 'bcqwpvgxtuvqosoj')
       smtp.send_message(msg)

## MAIN CALL
if __name__ == '__main__':
    try:
       print('##########################')
       print('### WEEDLE GRAPH ')
       print('##########################')
       print('###### CREATE TEMPERATURE GRAPH')
       createTrackerGraph('Temperature','Celcius')
       print('###### CREATE SOIL MOISTURE GRAPH')
       createTrackerGraph('Soil-Moisture','%')
       print('###### CREATE SOIL FERTILITY GRAPH')
       createTrackerGraph('Soil-Fertility','upS/cm')
       print('###### CREATE SUN GRAPH')
       createTrackerGraph('Sun','lux')
       print('###### SEND EMAIL WITH GRAPH')
       sendMail()
    except Exception as e: 
       print('##########################')
       print('### WEEDLE GRAPH EMAIL FAILED')
       print('### with issue ',e)	
       print('##########################')
       print('                          ')
       print('                          ')
