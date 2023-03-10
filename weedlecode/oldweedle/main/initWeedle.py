#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import sys

#Hot Air
Relay1Pin = 31
#Cold Air
Relay2Pin = 32
#Water
Relay3Pin = 33
#White Light
Relay4Pin = 35
#Blue Light
Relay5Pin = 37
#Red Light 
Relay6Pin = 38


def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setwarnings(False)
    GPIO.setup(Relay1Pin, GPIO.OUT)
    GPIO.setup(Relay2Pin, GPIO.OUT)
    GPIO.setup(Relay3Pin, GPIO.OUT)
    GPIO.setup(Relay4Pin, GPIO.OUT)
    GPIO.setup(Relay5Pin, GPIO.OUT)
    GPIO.setup(Relay6Pin, GPIO.OUT)

def action():
    print 'Weedle OFF...'
    GPIO.output(Relay1Pin, GPIO.LOW)
    GPIO.output(Relay2Pin, GPIO.LOW)
    GPIO.output(Relay3Pin, GPIO.LOW)
    GPIO.output(Relay4Pin, GPIO.LOW)
    GPIO.output(Relay5Pin, GPIO.LOW)
    GPIO.output(Relay6Pin, GPIO.LOW)
 
def destroy():
    GPIO.output(RelayPin, GPIO.LOW)
    #GPIO.cleanup()                     # Release resource

def configFile():
    # check if the config file exists if not create them with defaul
    try:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        #DAY CONFIG
        dayTimeLineConfigFile = currentDir + "/" + "config/daytimeline.config"
        dayInterfaceLineConfigFile = currentDir + "/" + "config/dayintervaleline.config"
        
        #daytimeline file
        if os.path.isfile( dayTimeLineConfigFile ):
            print 'Day Time Line Config in place'
        else:
            with open(dayTimeLineConfigFile, "w") as f:
                f.write('CALL ONCE weedleConfigUpdate.py')
                f.close()   

        #dayIntervaleline file
        if os.path.isfile( dayInterfaceLineConfigFile ):
            print 'Day Intervale line Config in place'
        else:
            with open(dayInterfaceLineConfigFile, "w") as f:
                f.write('CALL weedleAdjustment.py \n')
                f.write('CALL weedleDiagnostic.py')
                f.close()   


        #WEEDLE CONFIG
        weedleDayConfigFile = currentDir + "/" + "config/weedleDay.config"
        weedleAdjustmentConfigFile = currentDir + "/" + "config/weedleAdjustment.config"
        weedleClimateConfigFile = currentDir + "/" + "config/weedleClimate.config"
       
        #Weedle Day Config
        if os.path.isfile( weedleDayConfigFile ):
            print 'Weedle Day Config in place'
        else:
            with open(weedleDayConfigFile, "w") as f:
                f.write('CALL ONCE weedleSunON.py \n')
                f.write('CALL ONCE weedleSunOFF.py')
                f.close()   

        # Weedle Adjustment Config
        if os.path.isfile( weedleAdjustmentConfigFile ):
            print 'Weedle Adjustment Config in place'
        else:
            with open(weedleAdjustmentConfigFile, "w") as f:
                f.write("TO PUT DEFAULT")
                f.close()   
    
        # Weedle Climate Config
        if os.path.isfile( weedleClimateConfigFile ):
            print 'Weedle Climate Config in place'
        else:
            with open(weedleClimateConfigFile, "w") as f:
                f.write("TO PUT DEFAULT")
                f.close()   

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

def init():
    setup()
    try:
        action()
        configFile()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
    


if __name__ == '__main__':             # Program start from here
    init()
    #setup()
    #try:
    #    action()
    #    configFile()
    #except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    #    destroy()
