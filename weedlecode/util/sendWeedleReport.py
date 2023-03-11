from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from reportGenerator.deviceMetricTrackerGraph import createDeviceMetricTrackerGraph
from reportGenerator.weedleSchedulerGanttGraph import createSchedulerGanttGraph

import os.path
import smtplib

from datetime import date

def sendMail():
	
    currentDay = date.today()    
    # Set up the email
    msg = MIMEMultipart()

    msg['From'] = 'climate@gmail.com'
    msg['To'] = 'joel.dupont@gmail.com'
    msg['Subject'] = 'Weedle Capture'

    # Define the file paths of the images
    file_paths = ['/home/weedle/weedlecode/weedleReport/weedleScheduler'+str(currentDay)+'.png',
                  '/home/weedle/weedlecode/weedleReport/Temperature.png',
                  '/home/weedle/weedlecode/weedleReport/Soil-Moisture.png',
                  '/home/weedle/weedlecode/weedleReport/Soil-Fertility.png', 
                  '/home/weedle/weedlecode/weedleReport/Sun.png']

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
       print('### GENERATE WEEDLE REPORT ')
       print('##########################')
       print('                          ')
       print('######WEEDLE DEVICE METRIC TRACKER GRAPH')
       print('                          ')
       print('##########CREATE TEMPERATURE GRAPH')
       createDeviceMetricTrackerGraph('Temperature','Celcius')
       print('##########CREATE SOIL MOISTURE GRAPH')
       createDeviceMetricTrackerGraph('Soil-Moisture','%')
       print('##########CREATE SOIL FERTILITY GRAPH')
       createDeviceMetricTrackerGraph('Soil-Fertility','upS/cm')
       print('########## CREATE SUN GRAPH')
       createDeviceMetricTrackerGraph('Sun','lux')
       print('##########################')
       print('                          ')
       print('######WEEDLE SCHEDULER GRAPH')
       print('                          ')
       print('##########################')
       createSchedulerGanttGraph()
       print('##########################')
       print('                          ')
       print('######WEEDLE SEND REPORT')
       print('                          ')
       print('##########################')
       sendMail()
       

    except Exception as e: 
       print('##########################')
       print('### FAILED WEEDLE REPORT')
       print('### with issue ',e)	
       print('##########################')
       print('                          ')
       print('                          ')
