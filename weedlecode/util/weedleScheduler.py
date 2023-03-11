#!/usr/bin/env python
import time
import datetime
import math

import sqlite3

from datetime import date

def maintainWeedleActivity(activity):
 
    global currentTime
    currentTime = datetime.datetime.now()
    currentDay = date.today()    
    currentHour = currentTime.hour
    currentMinute=0
    currentMinute = currentTime.minute
    print('####################### ')
    print('## STARTING MAINTENANCE WEEDLE SCHEDULER at '+str(currentTime))
    print('####################### ')  
    # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    ###########################
    # Get the current state of run time  
    ###########################
    #check Element run time
    cursor = conn.execute("SELECT * FROM W_ACTVITY_RUNTIME WHERE DAY=? and ACTIVITY=?",
                         (str(currentDay),Eelement))
    w_ar_id=-1
    arTotalHourON= 0
    arTotalMinuteON= 0
    arTotalHourOFF= 0
    arTotalMinuteOFF= 0
    arTotalHourONOFF=0
    arTotalMinuteONOFF= 0
    
    for row in cursor:
        w_ar_id=row[0]
        arActivity=row[1]
        arDay=row[2]
        arTotalHourON=row[3] or 0
        arTotalMinuteON=row[4] or 0
        arTotalHourOFF=row[5] or 0
        arTotalMinuteOFF=row[6] or 0
        arTotalHourONOFF=row[7] or 0
        arTotalMinuteONOFF=row[8] or 0
    
  
        

    
    ###########################################
    # CHECK BEST PRACTICES OF THIS ACTIVITY
    ##########################################
    #check Element Time Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         (activity,'TIME',plantSize))
    minElementTime=-1
    maxElementTime=-1                     
    for row in cursor:
        minElementTime=row[4]
        maxElementTime=row[5]
        elementUnit=row[6]


    ###########################
    # CONSTRAINT TIME CONSTRAINT
    ###########################
    #check Constraint TIME_SAVING
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and STATE=?",
                         (activity,'TIME_SAVING'))
    tsStartHour=-1
    tsStopHour=-1                     
    for row in cursor:
        tsStartHour=row[3]
        tsStopHour=row[4]
        print('###### ACTIVITY CONSTRAINT TIME_SAVING tsStartHour: '+str(tsStopHour)+' tsStopHour'+str(tsStopHour))
    
    #check Constraint MAX_HOUR_PER_DAY_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and STATE=?",
                         (Eelement,'MAX_HOUR_PER_DAY_ON'))
    maxHourPerDay=-1
    for row in cursor:
        maxHourPerDay=row[5]
        print('###### ACTIVITY CONSTRAINT RUN MAX_HOUR_PER_DAY_ON:'+str(maxHourPerDay))

    #check Constraint MAX_MINUTE_PER_DAY_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and STATE=?",
                         (Eelement,'MAX_MINUTE_PER_DAY_ON'))
    maxMinutePerDay=-1
    for row in cursor:
        maxMinutePerDay=row[5]
        print('###### ACTIVITY CONSTRAINT RUN MAX_MINUTE_PER_DAY_ON:'+str(maxMinutePerDay))


    #check Constraint MAX_MINUTE_PER_HOUR_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and STATE=?",
                         (activity,'MAX_MINUTE_PER_HOUR_ON'))
    maxMinutePerHour=-1
    for row in cursor:
        maxMinutePerHour=row[5]
        print('###### ACTIVITY CONSTRAINT RUN MAX_MINUTE_PER_HOUR_ON:'+str(maxMinutePerHour))
        


   ###########################
    # RECOMMENDATION 
    ###########################
    #Get Weedle Recommendations
    cursor = conn.execute("SELECT * FROM W_RECOMMENDATION WHERE ELEMENT=? AND (STATE=? OR STATE=?) AND DAY=? AND HOUR=? order by PRIORITY",
                         (Eelement,'NEW','ACTIVE',str(currentTime.strftime("%Y-%m-%d")),currentHour))
    recId=-1
    recCheckName='NONE'
    recActionMinute=0
    row = cursor.fetchone()
    
    #for row in cursor:
    if row is not None:
        recId=row[0]
        recCheckName=row[1]
        recElement=row[2]
        recAction=row[3]
        recActionMinute=row[4]
        recRecommendation=row[5]
        recState=row[6]
        recDay=row[7]
        recHour=row[8]
        recMinute=row[9]
        recPriority=row[10]
        
        print('###### RECOMMENDATION: '+str(recRecommendation))

       
    ###########################
    # CALCULATE 
    ###########################
    #calculate new Element state
    turnOn=False
 
    # P1: if RECOMMENDATION is on Temperature or WATER then HIGH priority therefore execute as P1
    #print(' ## DEBUG recCheckName '+recCheckName+' recActionMinute '+str(recActionMinute)+' currentMinute '+str(currentMinute)) 
    #print(' ## DEBUG calRunTimeMinute/60 '+str(truncRunTimeHour)+' minElementTime '+str(minElementTime)+' maxElementTime '+str(maxElementTime)) 
    if recCheckName in ('TEMPERATURE','SOIL MOISTURE') and recActionMinute > currentMinute:
        print('###### WEEDLE RECOMMENDATION P'+str(recPriority)+' ACTION: '+recAction+' for '+str(recActionMinute)+' on '+activity)
        if recAction=='ON':
           turnOn=True
        elif recAction=='OFF':          
           turnOn=False
        #Now Update the recommendatino to DONE
        if recId!=-1:
          cursor = conn.execute("UPDATE W_RECOMMENDATION SET STATE=? WHERE W_R_ID=?",
                               ('ACTIVE',recId))
           
    # P2 check Constraint TIME_SAVING
    elif currentHour in range(tsStartHour,tsStopHour):
        print('###### ACTIVITY CONSTRAINT TIME_SAVING tsStartHour: '+str(tsStopHour)+' tsStopHour'+str(tsStopHour))
        turnOn=False       
    # P2: check constraint MAX_HOUR_PER_DAY_ON
    elif arTotalHourON >= maxHourPerDay and maxHourPerDay !=-1:
        print('###### ACTIVITY CONSTRAINT RUN MAX_HOUR_PER_DAY_ON:'+str(maxHourPerDay))
        turnOn=False
    # P2: check constraint MAX_MINUTE_PER_DAY_ON
    elif arTotalMinuteON >= maxMinutePerDay and maxMinutePerDay !=-1:
        print('###### ACTIVITY CONSTRAINT RUN MAX_HOUR_PER_DAY_ON:'+str(maxMinutePerDay))
        turnOn=False
    # P2: check constraint MAX_MINUTE_PER_DAY_ON
    elif currentMinute >= maxMinutePerHour and maxMinutePerHour!=-1:
        print('###### ACTIVITY CONSTRAINT RUN MAX_MINUTE_PER_HOUR_ON:'+str(maxMinutePerHour))
        turnOn=False
 
    # P4 if recommendation is on Temperature or WATER then HIGH priority therefore execute as P1
    elif recCheckName in ('SUN','SOIL FERTILITY') and recActionMinute < currentMinute:
        print('###### WEEDLE RECOMMENDATION P4 ACTION: '+recAction+' for '+str(recActionMinute)+' on '+activity)
        if recAction=='ON':
           turnOn=True
        elif recAction=='OFF':          
           turnOn=False
        #Now Update the recommendatino to DONE
        if recId!=-1:
          cursor = conn.execute("UPDATE W_RECOMMENDATION SET STATE=? WHERE W_R_ID=?",
                               ('ACTIVE',recId))
    
    else:
        print('###### ELSE STILL MORE '+Activity)
        turnOn=True
        #Now Update the recommendatino to DONE

    if recId!=-1:
       cursor = conn.execute("UPDATE W_RECOMMENDATION SET STATE=? WHERE W_R_ID=? and STATE <> 'ACTIVE'",
                            ('INACTIVE',recId))

    ###########################
    # SCHEDULE ACTIVITY PREPARTION  
    ###########################
    #check if activity is open
    cursor = conn.execute("SELECT * FROM W_WEEDLE_SCHEDULE WHERE ACTIVITY=? and DAY=? and STATE=? ",
                         (activity,str(currentDay),'Active'))
    ws_id=-1
    
    for row in cursor:
        ws_id=row[0]
        
    if ws_id==-1:
        print('###### INSERTING A TASK IN WEEDLE SCHEDULE FOR '+Activite+' DAY '+str(currentDay)+' START_HOUR '+str(currentHour)+' START_MINUTE '+str(currentMinute))
        conn.execute("INSERT INTO W_WEEDLE_SCHEDULER (ACTIVITY, STATE, DAY, START_HOUR, START_MINUTE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (activity,'Active', str(currentDay),currentHour,currentMinute))
    
   #get the id of the activity we need to work on
    cursor = conn.execute("SELECT * FROM W_WEEDLE_SCHEDULE WHERE ACTIVITY=? and DAY=? and STATE=? ",
                         (activity,str(currentDay),'Active'))
    ws_id=-1
    
    for row in cursor:
        ws_id=row[0]
        wsActivity=row[1]
        wsState=row[5] or 0
        wsDay=row[2]
        wsStartHour=row[3]
        wsStartMin=row[4] or 0
        wsStopHour=row[3]
        wsStopMin=row[4] or 0

    

    if w_ar_id==-1:
        print('###### INSERTING THE ACTIVITY RUN TIME FOR '+activity+' '+str(elementState)+' DAY '+str(currentDay)+' MIN '+str(currentMinute)+' Last Hour '+str(currentHour))
        conn.execute("INSERT INTO W_ACTIVITY_RUNTIME (ACTIVITY, DAY, TOTAL_HOUR_ON, TOTAL_MINUTE_ON, TOTAL_HOUR_OFF, TOTAL_MINUTE_OFF, TOTAL_HOUR_ONOFF, TOTAL_MINUTE_ONOFF) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (activity, str(currentDay), 0, 0, 0, 0, 0, 0))

    ###########################
    # SCHEDULE ACTIVITY UPDATE  
    ###########################
    
    if turnOn:

    else:
    
    # update with latest	 
    print('###### UPDATE THE RUN TIME FOR '+Eelement+' '+str(elementState)+' RunTime: '+str(calRunTime)+' RunTimeMinute: '+str(calRunTimeMinute)+' OffTime: '+str(offTime)+' LastHourCheck: '+str(currentHour)+' LastMinuteCheck '+str(currentMinute))
    conn.execute("UPDATE W_ELEMENT_RUNTIME SET STATE=?, RUN_TIME=?, RUN_TIME_MINUTE=?, OFF_TIME=?, LAST_MINUTE_CHECK=?, LAST_HOUR_CHECK=? WHERE AR_ID=?" ,
                 (str(elementState),calRunTime, calRunTimeMinute, offTime, currentMinute, currentHour,ar_id))
                 
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()
              
    print('                        ')
    print('                        ')
    
    
