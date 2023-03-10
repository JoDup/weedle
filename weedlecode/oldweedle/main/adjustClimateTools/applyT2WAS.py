import RPi.GPIO as GPIO
import time
import datetime
import math
import sys
sys.path.insert(0,'/home/pi/weedle/gardener/main')
sys.path.insert(1,'/home/pi/weedle/gardener/main/adjustClimateTools')

import config.readweedleAdjustment
import applyElements

import os

water = "0"
air = "0"
sun = "0"

def applyT2WAS(direction,adjustment):
    try:
        if direction == 'DECREASE':

            print "------------------------"
            print "= IN DECREASE TEMPERATURE"
            print "------------------------"
            water = config.readweedleAdjustment("Twater")
            air = config.readweedleAdjustment("Tair")
            sun = config.readweedleAdjustment("Tsun")
            print "============================"
            print "===  GARDENER TO EXECUTE ==="
            print "============================"
            print "==  water = "+ water
            print "==  air = "+ air
            print "==  sun = "+ sun
            print "============================"

        if direction == 'INCREASE':

            print "------------------------"
            print "= IN INCREASE TEMPERATURE"
            print "------------------------"
            water = config.readweedleAdjustment("TWater")
            air = config.readweedleAdjustment("TAir")
            sun = config.readweedleAdjustment("TSun")
            print "============================"
            print "===  GARDENER TO EXECUTE ==="
            print "============================"
            print "==  water = "+ water
            print "==  air = "+ air
            print "==  sun = "+ sun
            print "============================"


### APPLY WATER
        waterSec = int(water)*int(adjustment)
        print "---"
        print "###  Caculated WATER in Sec: " + str(waterSec) +" ###"
        print "---"
        applyElements.applyWater(waterSec)
        print "---"
### APPLY AIR
        airSec = int(air)*int(adjustment)
        print "###  Caculated AIR in Sec: " + str(airSec) +" ###"
        print "---"
        applyElements.applyAir(airSec)   
        print "---"
 
### APPLY Sun
        sunSec = int(sun)*int(adjustment)
        print "### Caculated SUN (hot Air) in Sec: " + str(sunSec) +" ###"
        print "---"
        applyElements.applySun(sunSec)    
        print "---"

### LOG THE ACTION
        currentDir = os.path.dirname(os.path.realpath(__file__))
        #GARDENER CONFIG
        #gardenerActions = currentDir + "/" + "logs/gardenerActions.log"
        gardenerActions = "/home/pi/weedle/gardener/main/logs/gardenerActions.log"
        with open(gardenerActions, "a") as f:
            f.write('T2WAS|'+str(datetime.datetime.now())+"|"
                    +direction+"|"+str(adjustment)+"|"
                    +str(water)+"|"
                    +str(air)+"|"
                    +str(sun)+"|"
                    +str(waterSec)+"|"
                    +str(airSec)+"|"
                    +str(sunSec)+"|END_ACTION|\n")
            f.close()
              


   
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

if __name__ == '__main__':             # Program start from here

    try:
        applyT2WAS('DECREASE',0)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
