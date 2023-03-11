import time
import datetime
import sqlite3

from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from datetime import date

#mac = '5C:85:7E:B0:40:38'

def insTracker(conn, name, value, bpmin, bpmax, unit):
	
    currentTime = datetime.datetime.now()

    #check if the trracker already exists for this hour
    cursor = conn.execute("SELECT * FROM W_DEVICE_METRIC_TRACKER WHERE NAME=? and DAY=? and HOUR=?",
	                     (name,str(currentTime.strftime("%Y-%m-%d")),currentTime.hour))
	                     
    w_mt_id = -1
    for row in cursor:
        w_mt_id=row[0]
                    
    if w_mt_id == -1:
        print('###### INSERTING THE METRIC TRACKER name: '+name+' value '+str(value)+' unit: '+unit)
        conn.execute("INSERT INTO W_DEVICE_METRIC_TRACKER (NAME, VALUE, UNIT, DAY, HOUR, BEST_PRACTICE_MIN, BEST_PRACTICE_MAX) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, value, unit,
                    str(currentTime.strftime("%Y-%m-%d")),currentTime.hour,bpmin, bpmax))
    else:
        print('###### UPDATE METRIC TRACKER with LATEST name: '+name+' value '+str(value)+' unit: '+unit)
        cursor = conn.execute("UPDATE W_DEVICE_METRIC_TRACKER SET VALUE=?, BEST_PRACTICE_MIN=?, BEST_PRACTICE_MAX=? WHERE NAME=? and DAY=? and HOUR=?",
	                         (value, bpmin, bpmax, name, str(currentTime.strftime("%Y-%m-%d")),currentTime.hour))


def insRecommendation(conn, checkName, element,action,actionMin,currentfeeling,bestPractice,unit,priority):
	
    currentTime = datetime.datetime.now()
#    conn.execute("update w_recommendation set state='OLD' and TIME <?",(currentHour,))

    recommendation = 'Weedle recommend to turn the '+action +' '+element+' for the next '+str(actionMin)+' min current  '+checkName+' Value: '+str(currentfeeling)+' '+str(unit)+' vs Best Practices '+str(bestPractice)+' '+str(unit)

    #check if the recommendation already exists for this hour
    cursor = conn.execute("SELECT * FROM W_WEEDLE_RECOMMENDATION WHERE CHECK_NAME=? and ELEMENT= ? and ACTION=? and ACTION_MINUTE=? and DAY=? and HOUR=?",
	                     (checkName,element,action,actionMin,str(currentTime.strftime("%Y-%m-%d")),currentTime.hour))
	                     
    w_r_id = -1
    for row in cursor:
        w_r_id=row[0]
                    
    if w_r_id == -1:
        print('###### INSERTING THE RECOMMENDATION Weedle recommend to turn the '+action+' '+element+' for the next '
                    +str(actionMin)+' min current  '+checkName+' Value: '+str(currentfeeling)+' '+str(unit)+' vs Best Practices '+str(bestPractice)+' '+str(unit))
        conn.execute("INSERT INTO W_WEEDLE_RECOMMENDATION (CHECK_NAME, ELEMENT, ACTION, ACTION_MINUTE, RECOMMENDATION, STATE, DAY, HOUR, MINUTE, PRIORITY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (checkName,element,action, actionMin,recommendation,
                    'NEW',str(currentTime.strftime("%Y-%m-%d")),currentTime.hour,currentTime.minute,priority))
    else:
        print('###### IN PLACE RECOMMENDATION Weedle recommend to turn the '+action+' '+element+' for the next '
                    +str(actionMin)+' min current  '+checkName+' Value: '+str(currentfeeling)+' '+str(unit)+' vs Best Practices '+str(bestPractice)+' '+str(unit))

def weedleRecommendation(conn, plantSize):
 
    global currentTime
    currentTime = datetime.datetime.now()
    currentDay = date.today()    
    currentHour = currentTime.hour
    currentMin = currentTime.minute
    print('####################### ')
    print('## STARTING RECOMMENDATION '+str(currentTime))
    print('####################### ')  
    
    # Connect to the database
    #conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
 
    conn.execute("delete from w_weedle_recommendation where date(day) < date('now','-3 days')")
 
    #get the mac of the device tracker
    cursor = conn.execute("SELECT * FROM W_WEEDLE_GARDEN WHERE ACTIVITY=? ",
			 ('DEVICE_METRIC',))
    mac = -1
    for row in cursor:
        mac=row[5]
    
    poller = MiFloraPoller(mac, BluepyBackend)
   
    #check Air Temperature Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         ('AIR','TEMPERATURE',plantSize))
    for row in cursor:
        BPminTemperature=row[4]
        BPmaxTemperature=row[5]
        BPTemperatureUnit=row[6]

    #check Soil Moisture Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         ('SOIL','MOISTURE',plantSize))
    for row in cursor:
        BPminSoilMoisture=row[4]
        BPmaxSoilMoisture=row[5]
        BPsoilMoistureUnit=row[6]

    #check Soil Fertility Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         ('SOIL','FERTILITY',plantSize))
    for row in cursor:
        BPminSoilFertility=row[4]
        BPmaxSoilFertility=row[5]
        BPsoilFertilityUnit=row[6]
 
    #check Soil Fertility Best Practices
    cursor = conn.execute("SELECT * FROM W_BEST_PRACTICE WHERE BP_OBJECT=? and BP_TYPE=? and PLANT_SIZE=?",
                         ('SUN','INTENSITY',plantSize))
    for row in cursor:
        BPminSun=row[4]
        BPmaxSun=row[5]
        BPsunUnit=row[6]

    temperature=poller.parameter_value('temperature')
    soilMoisture=poller.parameter_value('moisture')
    sun=poller.parameter_value('light')
    soilFertility=poller.parameter_value('conductivity')
    
    print('                        ')  
    print("FW: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}".format(temperature))
    print("Moisture: {}".format(soilMoisture))
    print("Light: {}".format(sun))
    print("Conductivity: {}".format(soilFertility))
    
    ###  INSERT IN TRACKER
    insTracker(conn,'Temperature',str(temperature),BPminTemperature,BPmaxTemperature,BPTemperatureUnit)
    insTracker(conn,'Soil-Moisture',str(soilMoisture),BPminSoilMoisture,BPmaxSoilMoisture,BPsoilMoistureUnit)
    insTracker(conn,'Sun',str(sun),BPminSun,BPmaxSun,BPsunUnit)
    insTracker(conn,'Soil-Fertility',str(soilFertility),BPminSoilFertility,BPmaxSoilFertility,BPsoilFertilityUnit)

    print('                        ')  
    print('### CHECK TEMPERATURE:   ')    
    if temperature > BPmaxTemperature:
	    insRecommendation(conn,'TEMPERATURE','SUN','OFF',30,temperature,BPmaxTemperature,BPTemperatureUnit,1)
	    insRecommendation(conn,'TEMPERATURE','AIR','ON',30,temperature,BPmaxTemperature,BPTemperatureUnit,1)
	    insRecommendation(conn,'TEMPERATURE','HOTAIR','0FF',59,temperature,BPminTemperature,BPTemperatureUnit,1)
    elif temperature < BPminTemperature:
	    insRecommendation(conn,'TEMPERATURE','SUN','ON',30,temperature,BPminTemperature,BPTemperatureUnit,1)
	    insRecommendation(conn,'TEMPERATURE','HOTAIR','ON',30,temperature,BPminTemperature,BPTemperatureUnit,1)
	    insRecommendation(conn,'TEMPERATURE','AIR','OFF',30,temperature,BPminTemperature,BPTemperatureUnit,1)
    else:
        print ('###### TEMPERATURE IS GOOD FOR '+str(temperature)+' vs Best Practices min: '+str(BPminTemperature)+' max: '+str(BPmaxTemperature)+' '+BPTemperatureUnit)

    print('                        ')  
    print('### CHECK SOIL MOISTURE:   ')    
    if soilMoisture > BPmaxSoilMoisture:
	    insRecommendation(conn,'SOIL MOISTURE','SUN','ON',30,soilMoisture,BPmaxSoilMoisture,BPsoilMoistureUnit,2)
	    insRecommendation(conn,'SOIL MOISTURE','AIR','ON',30,soilMoisture,BPmaxSoilMoisture,BPsoilMoistureUnit,2)
	    insRecommendation(conn,'SOIL MOISTURE','HOTAIR','ON',30,soilMoisture,BPminTemperature,BPTemperatureUnit,2)
    elif soilMoisture < BPminSoilMoisture:
	    insRecommendation(conn,'SOIL MOISTURE','WATER','ON',59,soilMoisture,BPminSoilMoisture,BPsoilMoistureUnit,2)
	    insRecommendation(conn,'SOIL MOISTURE','SUN','OFF',30,soilMoisture,BPminSoilMoisture,BPsoilMoistureUnit,2)
	    insRecommendation(conn,'SOIL MOISTURE','AIR','OFF',30,soilMoisture,BPminSoilMoisture,BPsoilMoistureUnit,2)
	    insRecommendation(conn,'SOIL MOISTURE','HOTAIR','OFF',59,soilMoisture,BPminTemperature,BPTemperatureUnit,2)
    else:
        print ('###### SOIL MOISTURE IS GOOD FOR '+str(soilMoisture)+' vs Best Practices min: '+str(BPminSoilMoisture)+' max: '+str(BPmaxSoilMoisture)+' '+BPsoilMoistureUnit)
    
    print('                        ')  
    print('### CHECK SUN :   ')    
    if sun > BPmaxSun:
	    insRecommendation(conn,'SUN','SUN','OFF',30,sun,BPmaxSun,BPsunUnit,3)
    elif sun < BPminSun:
	    insRecommendation(conn,'SUN','SUN','ON',59,sun,BPminSun,BPsunUnit,3)
    else:
        print ('###### SUN IS GOOD FOR '+str(sun)+' vs Best Practices min: '+str(BPminSun)+' max: '+str(BPminSun)+' '+BPsunUnit)

    print('                        ')  
    print('### CHECK SOIL FERTILITY :   ')    
    if soilFertility > BPmaxSoilFertility:
	    insRecommendation(conn,'SOIL FERTILITY','WATER','OFF',59,soilFertility,BPmaxSoilFertility,BPsoilFertilityUnit,4)
    elif soilFertility < BPminSoilFertility:
	    insRecommendation(conn,'SOIL FERTILITY','WATER','ON',59,soilFertility,BPminSoilFertility,BPsoilFertilityUnit,4)
    else:
        print ('###### SOIL FERTILITY IS GOOD FOR '+str(soilFertility)+' vs Best Practices min: '+str(BPminSoilFertility)+' max: '+str(BPmaxSoilFertility)+' '+BPsoilFertilityUnit)

    print('                        ')  
    print('           ====== END RECOMENDATION!');
    # Commit the changes
    #conn.commit()
    
    # Close the connection
    #conn.close()
                     
