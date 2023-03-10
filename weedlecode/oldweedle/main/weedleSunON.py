import RPi.GPIO as GPIO
import time
import math
import datetime
import elements.sun.redlightON
import elements.sun.bluelightON
import elements.sun.whitelightON
import config.readweedleClimate
import os
import sys


WSunriseRED = "0FF"
WSunriseBLUE = "0FF"
WSunriseWHITE = "0FF"

if __name__ == '__main__':             # Program start from here

    print  "############################"
    print ('##### IN WEEDLE SUNRISE ####')
    print  "############################"

    try:
#### READ CLIMATE FROM CONFIG
#### SUNSET        
        WSunriseRED = config.readweedleClimate("WSunriseRED")
        WSunriseBLUE = config.readweedleClimate("WSunriseBLUE")
        WSunriseWHITE = config.readweedleClimate("WSunriseWHITE")
        print "####    WEEDLE SUNRISE  #####"
        print "#############################"
        print "##  WSunsetRED = "+ WSunriseRED
        print "##  WSunsetBLUE = "+ WSunriseBLUE
        print "##  WSunsetWHITE = "+ WSunriseWHITE
        print "#############################"

        
        if WSunriseRED == "ON":
            print "Turn ON RedSUN"
            elements.sun.redlightON.action()
            print "----"
        else:
            print "Turn OFF RedSUN"
            print "----"
            
        if WSunriseBLUE == "ON":
            print "Turn ON BlueSUN"
            elements.sun.bluelightON.action()
            print "----"
        else:
            print "Turn OFF BlueSUN"
            print "----"

        if WSunriseWHITE == "ON":
            print "Turn On whiteSUN"
            elements.sun.whitelightON.action()
            print "----"
        else:
            print "Turn OFF whiteSUN"
            print "----"


### LOG THE ACTION
        currentDir = os.path.dirname(os.path.realpath(__file__))
        #GARDENER CONFIG
        gardenerActions = currentDir + "/" + "logs/gardenerActions.log"
        with open(gardenerActions, "a") as f:
            f.write('SUNRISE|'+str(datetime.datetime.now())+"|"+WSunriseRED+"|"+WSunriseBLUE+"|"+WSunriseWHITE+"|END_ACTION|\n")
            f.close()
       
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

