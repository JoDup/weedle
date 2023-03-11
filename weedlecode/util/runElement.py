#!/usr/bin/env python

import time
import datetime
import math

import sqlite3

from pyHS100 import SmartStrip

from datetime import date

def runElement(plantSize, Eelement, Eindex):
 
    global currentTime
    currentTime = datetime.datetime.now()
    currentDay = date.today()    
    currentHour = currentTime.hour
    currentMinute=0
    currentMinute = currentTime.minute
    print('####################### ')
    print('## STARTING '+Eelement+' CHECK at '+str(currentTime))
    print('####################### ')  
    # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    #connect to the strip
    gardener = SmartStrip("172.27.0.69")

    #get state of Element
    elementState = gardener.is_on(index=Eindex)
    
    
    #check Element Time Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         (Eelement,'TIME',plantSize))
    for row in cursor:
        minElementTime=row[4]
        maxElementTime=row[5]
        unit=row[6]

    #check Element run time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_RUNTIME WHERE DAY=? and ELEMENT=?",
                         (str(currentDay),Eelement))
    ar_id=-1
    runTime=0
    runTimeMinute=0
    calRunTime=0
    calRunTimeMinute=0
    offTime=0
    
    for row in cursor:
        ar_id=row[0]
        rtElement=row[1]
        rtElementState=row[2]
        day=row[3]
        runTime=row[4] or 0
        runTimeMinute=row[5] or 0
        offTime=row[6]
        lastHourCheck=row[7]
        lastMinuteCheck=row[8]
    
    calRunTime=runTime
    calRunTimeMinute=runTimeMinute
    ###########################
    # TIME PREPARTION  
    ###########################
        
    if ar_id==-1:
        print('###### INSERTING THE RUN TIME FOR '+Eelement+' '+str(elementState)+' DAY '+str(currentDay)+' MIN '+str(currentMinute)+' Last Hour '+str(currentHour))
        conn.execute("INSERT INTO W_ELEMENT_RUNTIME (ELEMENT, STATE, DAY, RUN_TIME, RUN_TIME_MINUTE, OFF_TIME, LAST_MINUTE_CHECK, LAST_HOUR_CHECK) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (Eelement,str(elementState), str(currentDay), 0, 0, 0, currentMinute, currentHour))
    else:
        diffHour = currentHour-lastHourCheck
        diffMinute  = currentMinute-lastMinuteCheck
       
        if (elementState) and rtElementState=='True':
			#new runtime
            if diffHour != 0:
               calRunTime=0
               calRunTime=runTime+diffHour
            print('###### SET RUN TIME '+str(runTime))
            
            #new runtimeminute
            #if currentHour==0 and runTimeMinute > 59:
            #   calRunTimeMinute=0
            if diffHour == 0 and diffMinute != 0:
               calRunTimeMinute=0
               calRunTimeMinute=int(runTimeMinute)+int(diffMinute)
            print('###### SET RUN TIME MINUTE '+str(calRunTimeMinute)+' DEBUG runTimeMinute: '+str(runTimeMinute)+' diffMinute: '+str(diffMinute)+' currentHour: '+str(currentHour))
   
        elif not(elementState) and rtElementState=='False' and diffHour != 0:
            print('###### SET OFFTIME TIME '+str(offTime))
            offTime=offTime+diffHour
            
    #calculate the total run time by adding the min
    #minToHour=0
    #if runTimeMinute is not None:
    #   minToHour = int(runTimeMinute)/60
    #new Run Time with minute added          
    #CalRunTime = int(runTime) + minToHour
       

    ###########################
    # CONSTRAINT 
    ###########################
    #check Constrain Element off run time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_CONSTRAINT WHERE ELEMENT=? and STATE=?",
                         (Eelement,'OFF'))
    consStartTime=-1
    consStopTime=-1                     
    for row in cursor:
        consStartTime=row[3]
        consStopTime=row[4]
    
    #check Constrain Element for OneTime max minute time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_CONSTRAINT WHERE ELEMENT=? and STATE=?",
                         (Eelement,'ONE_TIME'))
    minuteOneTime=-1
    for row in cursor:
        minuteOneTime=row[5]
        print('###### ONE TIME RUN MIN:'+str(minuteOneTime))
        
    #check Constrain Element for Max Minute in Day max min time
    cursor = conn.execute("SELECT * FROM W_ELEMENT_CONSTRAINT WHERE ELEMENT=? and STATE=?",
                         (Eelement,'MAX_MINUTE_ON'))
    maxMinuteTime=-1
    for row in cursor:
        maxMinuteTime=row[5]
        print('###### MAX TIME RUN MINUTE:'+str(maxMinuteTime))
 
 
    ###########################
    # RECOMMENDATION 
    ###########################
    #Get Weedle Recommendations
    cursor = conn.execute("SELECT * FROM W_WEEDLE_RECOMMENDATION WHERE ELEMENT=? AND (STATE=? OR STATE=?) AND DAY=? AND HOUR=? order by PRIORITY",
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
    truncRunTimeHour = math.floor(calRunTimeMinute / 60)
 
    # P1: if RECOMMENDATION is on Temperature or WATER then HIGH priority therefore execute as P1
    #print(' ## DEBUG recCheckName '+recCheckName+' recActionMinute '+str(recActionMinute)+' currentMinute '+str(currentMinute)) 
    #print(' ## DEBUG calRunTimeMinute/60 '+str(truncRunTimeHour)+' minElementTime '+str(minElementTime)+' maxElementTime '+str(maxElementTime)) 
    if recCheckName in ('TEMPERATURE','SOIL MOISTURE') and recActionMinute > currentMinute:
        print('###### WEEDLE RECOMMENDATION P'+str(recPriority)+' ACTION: '+recAction+' for '+str(recActionMinute)+' on '+Eelement)
        if recAction=='ON':
           turnOn=True
        elif recAction=='OFF':          
           turnOn=False
        #Now Update the recommendatino to DONE
        if recId!=-1:
          cursor = conn.execute("UPDATE W_WEEDLE_RECOMMENDATION SET STATE=? WHERE W_R_ID=?",
                               ('ACTIVE',recId))
           
    # P2: check Time Saving OFF CONSTRAINT		
    elif currentHour in range(consStartTime,consStopTime):
        print('###### CONTRAINT TIME SAVING: TURN OFF '+Eelement)
        turnOn=False
        
    # P2: check time Max Minute ON CONSTRAINT		
    elif calRunTimeMinute >= maxMinuteTime and maxMinuteTime!=-1:
        print('###### CONSTRAINT TIME MAX MINUTE: TURN OFF '+Eelement)
        turnOn=False
        
    # P3: check the BEST PRACTICE on TIME     ## TO REVIEW TO HANDLE THE RANGE   
    elif truncRunTimeHour >= minElementTime or truncRunTimeHour>= maxElementTime:
        print('###### BEST PRACTICE MIN MAX HOUR TIME: TURN OFF '+Eelement)
        turnOn=False
 
    # P3: Check for this hour if the CONSTRAINT ONE Time is respected    
    elif currentMinute >= minuteOneTime and minuteOneTime != -1:
	    print('###### CONTRAINT MAX ONE MINUTE RUN: TURN OFF '+Eelement)
	    turnOn=False
 
    # P4 if recommendation is on Temperature or WATER then HIGH priority therefore execute as P1
    elif recCheckName in ('SUN','SOIL FERTILITY') and recActionMinute < currentMinute:
        print('###### WEEDLE RECOMMENDATION P4 ACTION: '+recAction+' for '+str(recActionMinute)+' on '+Eelement)
        if recAction=='ON':
           turnOn=True
        elif recAction=='OFF':          
           turnOn=False
        #Now Update the recommendatino to DONE
        if recId!=-1:
          cursor = conn.execute("UPDATE W_WEEDLE_RECOMMENDATION SET STATE=? WHERE W_R_ID=?",
                               ('ACTIVE',recId))
    
    else:
        print('###### ELSE STILL MORE '+Eelement)
        turnOn=True
        #Now Update the recommendatino to DONE

    if recId!=-1:
       cursor = conn.execute("UPDATE W_WEEDLE_RECOMMENDATION SET STATE=? WHERE W_R_ID=? and STATE <> 'ACTIVE'",
                            ('INACTIVE',recId))
    
    if turnOn:
        gardener.turn_on(index=Eindex)
    else:
	    gardener.turn_off(index=Eindex)
    
    #get state of Element
    elementState = gardener.is_on(index=Eindex)
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
    
    
