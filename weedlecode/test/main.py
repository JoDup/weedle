#!/usr/bin/env python

import os
import sys
import time
import datetime

import sqlite3

from subprocess import call
from time import sleep
from pyHS100 import SmartStrip

#from command import Command
from datetime import date


FIELD_SEPARATOR="|"

timeDictionary = {}
intervalDictionary = {}
currentTimeString = ""

water = 0
air = 1
sun = 2



# Simple function to get and format the current time
def getTime():
    return datetime.datetime.now()
    
def convertTimeToString( time ):
    timeString = ""

    if ( time.hour < 10 ):
        timeString = currentTimeString + "0"

    timeString = timeString + str(time.hour) + ":"

    if ( time.minute < 10 ):
        timeString = timeString + "0"

    timeString = timeString + str(time.minute)

    return timeString

def init():
    global currentTime
    currentTime = getTime()
    currentDay = date.today()    
    currentHour = currentTime.hour
    currentMin = currentTime.minute

    print('## STARTING SUN CHECK at '+str(currentTime))
  
    # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    #connect to the strip
    gardener = SmartStrip("172.27.0.69")

    #get state of sun
    sunState = gardener.is_on(index=1)
    
    
    #check Sun Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         ('SUN','TIME','SMALL'))
    for row in cursor:
        minSunTime=row[4]
        maxSunTime=row[5]
        unit=row[6]

    #check Sun run time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_RUNTIME WHERE DAY=? and ELEMENT=?",
                         (str(currentDay),'SUN'))
    ar_id=-1
    runTime=0
    for row in cursor:
        ar_id=row[0]
        element=row[1]
        elementState=row[2]
        day=row[3]
        runTime=row[4]
        offTime=row[5]
        minHour=row[6]
        lastHourCheck=row[7]
        
    if ar_id==-1:
        print('######INSERTING THE RUN TIME FOR SUN '+str(sunState)+' DAY '+str(currentDay)+' MIN '+str(currentMin)+' Last Hour '+str(currentHour))
        conn.execute("INSERT INTO W_ELEMENT_RUNTIME (ELEMENT, STATE, DAY, RUN_TIME, OFF_TIME,MINUTE_CURRENT_HOUR, LAST_HOUR_CHECK) VALUES (?, ?, ?, ?, ?,?,?)",
                    ('SUN',str(sunState), str(currentDay), 0, 0, 0, currentMin, currentHour))
    else:
        diffHour = currentHour-lastHourCheck
       
        if (sunState) and elementState=='True' and diffHour != 0:
            print('######SET RUN TIME '+str(runTime))
            runTime=runTime+diffHour	    	
        elif not(sunState) and elementState=='False' and diffHour != 0:
            print('######SET OFFTIME TIME '+str(offTime))
            offTime=offTime+diffHour	
        print('######UPDATE THE RUN TIME FOR SUN '+str(sunState)+' Run Time '+str(runTime)+' OffTime '+str(offTime)+' MIN '+str(currentMin)+' Last Hour '+str(currentHour))
        conn.execute("UPDATE W_ELEMENT_RUNTIME SET STATE=?, RUN_TIME=?, OFF_TIME=?, MINUTE_CURRENT_HOUR=?, LAST_HOUR_CHECK=? WHERE AR_ID=?" ,
                    (str(sunState),runTime, offTime, currentMin, currentHour,ar_id))

    #check Sun run time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_CONSTRAINT WHERE ELEMENT=? and STATE=?",
                         ('SUN','OFF'))
    for row in cursor:
        consStartTime=row[3]
        consStopTime=row[4]
                   
    #calculate new Sun state
    if currentHour in range(consStartTime,consStopTime):
        print('######SAVING TURN OFF SUN')
        gardener.turn_off(index=sun)
    elif runTime in range (minSunTime,maxSunTime):
        print('###### LESS SUN ')
        gardener.turn_off(index=sun)
    else:
        print('###### MORE SUN ')
        gardener.turn_on(index=sun)
    
	
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
    
if __name__ == '__main__':
    init()
