#!/usr/bin/env python
import time
import datetime
import math

import sqlite3

from datetime import date

def maintainWeedleSchedule(conn, plantSize,activity):
 
    global currentTime
    currentTime = datetime.datetime.now()
    currentDay = date.today()   
    currentHour = 0 
    currentHour = currentTime.hour
    currentMinute=0
    currentMinute = currentTime.minute
    print('####################### ')
    print('## STARTING MAINTENANCE WEEDLE SCHEDULER at '+str(currentTime))
    print('####################### ')  
    # Connect to the database
    #conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    ###########################
    # Get the current state of run time  
    ###########################
    #check Element run time
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_RUNTIME WHERE DAY=? and ACTIVITY=?",
                         (str(currentDay),activity))
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
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_BEST_PRACTICE WHERE ACTIVITY=? and BEST_PRACTICE=? and PLANT_SIZE=?",
                         (activity,'TIME',plantSize))
    elementMinHour=-1
    elementMaxHour=-1                     
    for row in cursor:
        elementMinHour=row[4]
        elementMaxHour=row[5]
        elementUnit=row[6]


    ###########################
    # CONSTRAINT TIME CONSTRAINT
    ###########################
    #check Constraint TIME_SAVING
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE  ACTIVITY=? and CONSTRAINT_NAME=?",
                         (activity,'TIME_SAVING'))
    tsStartHour=-1
    tsStopHour=-1                     
    for row in cursor:
        tsStartHour=row[4]
        tsStopHour=row[5]
        print('###### ACTIVITY CONSTRAINT TIME_SAVING tsStartHour: '+str(tsStartHour)+' tsStopHour'+str(tsStopHour))
    
    #check Constraint MAX_HOUR_PER_DAY_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and CONSTRAINT_NAME=?",
                         (activity,'MAX_HOUR_PER_DAY_ON'))
    maxHourPerDay=-1
    for row in cursor:
        maxHourPerDay=row[6]
        print('###### ACTIVITY CONSTRAINT RUN MAX_HOUR_PER_DAY_ON:'+str(maxHourPerDay))

    #check Constraint MAX_MINUTE_PER_DAY_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and CONSTRAINT_NAME=?",
                         (activity,'MAX_MINUTE_PER_DAY_ON'))
    maxMinutePerDay=-1
    for row in cursor:
        maxMinutePerDay=row[7]
        print('###### ACTIVITY CONSTRAINT RUN MAX_MINUTE_PER_DAY_ON:'+str(maxMinutePerDay))


    #check Constraint MAX_MINUTE_PER_HOUR_ON
    cursor = conn.execute("SELECT * FROM W_ACTIVITY_CONSTRAINT WHERE ACTIVITY=? and CONSTRAINT_NAME=?",
                         (activity,'MAX_MINUTE_PER_HOUR_ON'))
    maxMinutePerHour=-1
    for row in cursor:
        maxMinutePerHour=row[7]
        print('###### ACTIVITY CONSTRAINT RUN MAX_MINUTE_PER_HOUR_ON:'+str(maxMinutePerHour))
        


   ###########################
    # RECOMMENDATION 
    ###########################
    #Get Weedle Recommendations
    cursor = conn.execute("SELECT * FROM W_WEEDLE_RECOMMENDATION WHERE ELEMENT=? AND (STATE=? OR STATE=?) AND DAY=? AND HOUR=? order by PRIORITY",
                         (activity,'NEW','ACTIVE',str(currentTime.strftime("%Y-%m-%d")),currentHour))
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
    # CALCULATE STATE
    ###########################
    #calculate new Element state
    turnOn=False
    
    currentHour = int(currentHour)
    tsStartHour = int(tsStartHour)
    tsStopHour = int(tsStopHour)

 
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
        print('###### ACTIVITY CONSTRAINT TIME_SAVING tsStartHour: '+str(tsStartHour)+' tsStopHour'+str(tsStopHour))
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
    # P3: check the BEST PRACTICE on TIME   
    elif arTotalHourON in range(elementMinHour, elementMaxHour):
        print('###### BEST PRACTICE MIN MAX HOUR TIME: TURN OFF '+activity)
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
          cursor = conn.execute("UPDATE W_WEEDLE_RECOMMENDATION SET STATE=? WHERE W_R_ID=?",
                               ('ACTIVE',recId))
    
    else:
        print('###### NO CONSTRAINT STILL MORE '+activity)
        turnOn=True
        #Now Update the recommendatino to DONE

    if recId!=-1:
       cursor = conn.execute("UPDATE W_WEEDLE_RECOMMENDATION SET STATE=? WHERE W_R_ID=? and STATE <> 'ACTIVE'",
                            ('INACTIVE',recId))

    ###########################
    # SCHEDULE ACTIVITY UPDATE  
    ###########################
    #check if activity is open
    cursor = conn.execute("SELECT * FROM W_WEEDLE_SCHEDULER WHERE ACTIVITY=? and DAY=? and STATE=? ",
                         (activity,str(currentDay),'Active'))
    w_ws_id=-1
    
    wsDay=0
    wsStartHour=0
    wsStartMinute=0 
    wsEndHour=0
    wsEndMinute=0
    
    for row in cursor:
        w_ws_id=row[0]
        wsActivity=row[1]
        wsState=row[2]
        wsDay=row[3]
        wsStartHour=row[4]
        wsEndHour=row[5] 
        wsStartMinute=row[6] 
        wsEndMinute=row[7]

    #print('DEBUG '+str(w_ws_id))
    #print('str(currentDay) '+str(currentDay))
    #print('wsDay '+str(wsDay))
    
    #If needs to be ON and activity does not exist 
    if turnOn and w_ws_id==-1:
        print('###### INSERTING A TASK IN WEEDLE SCHEDULE FOR '+activity+' DAY '+str(currentDay)+' START_HOUR '+str(currentHour)+' START_MINUTE '+str(currentMinute))
        conn.execute("INSERT INTO W_WEEDLE_SCHEDULER (ACTIVITY, STATE, DAY, START_HOUR, START_MINUTE) VALUES (?, ?, ?, ?, ?)",
                    (activity,'Active', str(currentDay),currentHour,currentMinute))
    #If needs to be ON and activity exist 
    elif turnOn and w_ws_id!=-1:
        print('###### NOTHING TO DO ACTIVE ACTIVITY '+activity+' EXIST FOR DAY '+str(wsDay)+' START_HOUR '+str(wsStartHour)+' START_MINUTE '+str(wsStartMinute)+' END_HOUR '+str(wsEndHour)+' END_MINUTE '+str(wsEndMinute))

    #If needs to be OFF and activity does not exist 
    elif not(turnOn) and w_ws_id==-1:
        print('###### NO TASK EXISTS YET SCENARIO '+activity+' EXIST FOR DAY '+str(wsDay)+' START_HOUR '+str(wsStartHour)+' START_MINUTE '+str(wsStartMinute)+' END_HOUR '+str(wsEndHour)+' END_MINUTE '+str(wsEndMinute))

    #If needs to be OFF and activity exist 
    elif not(turnOn) and w_ws_id!=-1:
        print('###### TURN OFF ACTIVITY '+activity+' EXIST FOR DAY '+str(wsDay)+' START_HOUR '+str(wsStartHour)+' START_MINUTE '+str(wsStartMinute)+' END_HOUR '+str(wsEndHour)+' END_MINUTE '+str(wsEndMinute))
        conn.execute("UPDATE W_WEEDLE_SCHEDULER SET STATE=?, END_HOUR=?, END_MINUTE=? WHERE w_ws_id=?",
                    ('Inactive', currentHour, currentMinute, w_ws_id))

   
   
    ###########################
    # UPDATE ACTIVITY RUNTIME  
    ###########################
 
    if w_ar_id==-1:
        print('###### INSERTING THE ACTIVITY RUN TIME FOR '+activity+' DAY '+str(currentDay)+' MIN '+str(currentMinute)+' Last Hour '+str(currentHour))
        conn.execute("INSERT INTO W_ACTIVITY_RUNTIME (ACTIVITY, DAY, TOTAL_HOUR_ON, TOTAL_MINUTE_ON, TOTAL_HOUR_OFF, TOTAL_MINUTE_OFF, TOTAL_HOUR_ONOFF, TOTAL_MINUTE_ONOFF) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (activity, str(currentDay), 0, 0, 0, 0, 0, 0))
    else:
        # update with latest
        #check if activity is open
        cursor = conn.execute("SELECT * FROM W_WEEDLE_SCHEDULER WHERE ACTIVITY=? and DAY=? ",
                             (activity,str(currentDay)))
        #resetTotal
        arTotalHourON=0
        arTotalMinuteON=0                     
        for row in cursor:
            wsStartHour=row[4]
            wsEndHour=row[5] or currentHour
            #print('DEBUG :'+str(wsStartHour))
            #print('DEBUG :'+str(wsEndHour))
            diff = wsEndHour - wsStartHour
            arTotalHourON= arTotalHourON + diff
            arTotalMinuteON= arTotalMinuteON + math.floor(diff*60)
        
        arTotalHourOFF= 24 - arTotalHourON
        arTotalMinuteOFF= 3600 - arTotalMinuteON
        arTotalHourONOFF= arTotalHourON + arTotalHourOFF
        arTotalMinuteONOFF= arTotalMinuteON + arTotalMinuteOFF
        print('###### UPDATE THE RUN TIME FOR '+activity
        +' arTotalHourON: '+str(arTotalHourON)+' arTotalMinuteON: '+str(arTotalMinuteON)
        +' arTotalHourOFF: '+str(arTotalHourOFF)+' arTotalMinuteOFF: '+str(arTotalMinuteOFF)
        +' arTotalHourONOFF '+str(arTotalHourONOFF) +' arTotalMinuteONOFF '+str(arTotalMinuteONOFF))
        conn.execute("UPDATE W_ACTIVITY_RUNTIME SET   TOTAL_HOUR_ON=?, TOTAL_MINUTE_ON=?, TOTAL_HOUR_OFF=?, TOTAL_MINUTE_OFF=?, TOTAL_HOUR_ONOFF=? , TOTAL_MINUTE_ONOFF=? WHERE W_AR_ID=?" ,
                 (arTotalHourON, arTotalMinuteON, arTotalHourOFF, arTotalMinuteOFF, arTotalHourONOFF, arTotalMinuteONOFF, w_ar_id))
                 
    ###########################
    # UPDATE ACTIVITY RUNTIME  
    ###########################
    ## Close previous day segment
    cursor = conn.execute("UPDATE W_WEEDLE_SCHEDULER SET STATE=?, END_HOUR=? WHERE END_HOUR IS NULL and DAY !=?",
                         ('INACTIVE',24,str(currentDay)))
    print('                        ')
    print('                        ')
    
#if __name__ == '__main__':
#    maintainWeedleActivity('SUN','SMALL')    
