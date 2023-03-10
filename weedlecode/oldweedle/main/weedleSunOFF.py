import RPi.GPIO as GPIO
import time
import datetime
import math
import elements.sun.redlightOFF
import elements.sun.bluelightOFF
import elements.sun.whitelightOFF
import config.readweedleClimate
import os
import sys

WSunsetRED = "0FF"
WSunsetBLUE = "0FF"
WSunsetWHITE = "0FF"

if __name__ == '__main__':             # Program start from here
    
    print  "#######################################"
    print ('#####    IN WEEDLE SUNSET          ####')
    print  "#######################################"
   
    try:
        
#### READ CLIMATE FROM CONFIG
#### SUNSET        
        WSunsetRED = config.readweedleClimate("WSunsetRED")
        WSunsetBLUE = config.readweedleClimate("WSunsetBLUE")
        WSunsetWHITE = config.readweedleClimate("WSunsetWHITE")
        print "####    WEEDLE SUNSET  #####"
        print "############################"
        print "##  WSunsetRED = "+ WSunsetRED
        print "##  WSunsetBLUE = "+ WSunsetBLUE
        print "##  WSunsetWHITE = "+ WSunsetWHITE
        print "############################"
        
        if WSunsetRED == "OFF":
            print "##  Turn OFF RedSUN"
            elements.sun.redlightOFF.action()
            print "----"
        else:
            print "##  Turn ON RedSUN"
            print "----"
            
        if WSunsetBLUE == "OFF":
            print "## Turn OFF BlueSUN"
            elements.sun.bluelightOFF.action()
            print "----"
        else:
            print "##  Turn ON BlueSUN"
            print "----"

        if WSunsetWHITE == "OFF":
            print "##  Turn OFF whiteSUN"
            elements.sun.whitelightOFF.action()
            print "----"
        else:
            print "##  Turn ON whiteSUN"
            print "----"
### LOG THE ACTION
            
        currentDir = os.path.dirname(os.path.realpath(__file__))
        #GARDENER CONFIG
        gardenerActions = currentDir + "/" + "logs/gardenerActions.log"
        with open(gardenerActions, "a") as f:
            f.write('SUNSET|'+str(datetime.datetime.now())+"|"+WSunsetRED+"|"+WSunsetBLUE+"|"+WSunsetWHITE+"|END_ACTION|\n")
            f.close()
            
        #time.sleep(int(hotair))
       
        #print "Call Hot Air On"
        #elements.hotairOFF.action()
       
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

