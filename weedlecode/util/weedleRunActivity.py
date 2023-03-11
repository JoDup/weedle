#!/usr/bin/env python

import time
import datetime
import math

import sqlite3

from pyHS100 import SmartStrip

from datetime import date

def weedleRunActivity(conn, plantSize, activity):
 
    global currentTime
    currentTime = datetime.datetime.now()
    currentDay = date.today()    
    currentHour = currentTime.hour
    currentMinute=0
    currentMinute = currentTime.minute
    print('####################### ')
    print('## STARTING '+activity+' CHECK at '+str(currentTime))
    print('####################### ')  
    # Connect to the database
    #conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    #connect to the strip
    #get the mac of the device tracker
    cursor = conn.execute("SELECT * FROM W_WEEDLE_GARDEN WHERE ACTIVITY=? ",
			 (activity,))

    ipAddress = -1
    Aindex = -1
    for row in cursor:
        ipAddress=row[7]
        Aindex=row[4]
    
    print('######### IPADDRESS :'+ str(ipAddress) +' Index Device: '+ str(Aindex))    
    gardener = SmartStrip(ipAddress)

    #get state of Element
    activityState = gardener.is_on(index=Aindex)
 
     #get the mac of the device tracker
    cursor = conn.execute("SELECT * FROM W_WEEDLE_SCHEDULER WHERE ACTIVITY=? AND DAY=? AND START_HOUR <=? AND IFNULL(END_HOUR,?)>=? AND STATE='Active' ",
			 (activity,str(currentDay),currentHour,currentHour,currentHour))
   
    w_ws_id = -1
    for row in cursor:
        w_ws_id=row[0]

    print('######### SCHEDULER FOUND :'+ str(w_ws_id)    )
    if w_ws_id==-1:
        print('################ TURN OFF DEVICE :'+ activity)    
        cursor = conn.execute("UPDATE W_WEEDLE_SCHEDULER SET WEEDLE_ACTION=? WHERE W_WS_ID=?",
			 ('PICKED_UP',w_ws_id))
       #gardener.turn_off(index=Aindex)
    else:
        print('################ TURN ON DEVICE :'+ activity)    
	    #gardener.turn_on(index=Aindex)
    
    # Commit the changes
    #conn.commit()
    
    # Close the connection
    #conn.close()
              
    print('                        ')
    print('                        ')
    
    
