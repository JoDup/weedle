import RPi.GPIO as GPIO
import time
import math
import os
import sys


def readweedleClimate(W2THCL):

    print (" == IN READ WEEDLE CLIMATE  == ")
    try:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        weedleAdjustConfigFile = currentDir + "/" + "weedleClimate.config"
        
        if os.path.isfile( weedleAdjustConfigFile ):
            with open(weedleAdjustConfigFile, "r") as f:
#### WEDDLE CLIMATE HIGH #####                
                if W2THCL == 'WTemperature':
                    WTemperature = f.read().split('\n')[0]
                    print "##  Read Weedle WTemperature:" + WTemperature
                    return WTemperature

                elif W2THCL == 'WHumidityAir':
                    WHumidityAir = f.read().split('\n')[1]
                    print "##  Read Weedle WHumidityAir:" + WHumidityAir
                    return WHumidityAir

                elif W2THCL == 'WHumiditySoil':
                    WHumiditySoil = f.read().split('\n')[2]
                    print "##  Read Weedle WHumiditySoil:" + WHumiditySoil
                    return WHumiditySoil

                elif W2THCL == 'WCO2':
                    WCO2 = f.read().split('\n')[3]
                    print "##  Read Weedle WCO2:" + WCO2
                    return WCO2

                elif W2THCL == 'WLuminosity':
                    WLuminosity = f.read().split('\n')[4]
                    print "##  Read Weedle WLuminosity:" + WLuminosity
                    return WLuminosity
#### WEEDLE CLIMATE LOW #####                
                if W2THCL == 'Wtemperature':
                    Wtemperature = f.read().split('\n')[5]
                    print "##  Read Weedle Wtemperature:" + Wtemperature
                    return Wtemperature

                elif W2THCL == 'Whumidityair':
                    Whumidityair = f.read().split('\n')[6]
                    print "##  Read Weedle Whumidity:" + Whumidityair
                    return Whumidityair

                elif W2THCL == 'Whumiditysoil':
                    Whumiditysoil = f.read().split('\n')[7]
                    print "##  Read Weedle Whumiditysoil:" + Whumiditysoil
                    return Whumiditysoil

                elif W2THCL == 'Wco2':
                    Wco2 = f.read().split('\n')[8]
                    print "##  Read Weedle Wco2:" + Wco2
                    return Wco2

                elif W2THCL == 'Wluminosity':
                    Wluminosity = f.read().split('\n')[9]
                    print "##  Read Weedle Wluminosity:" + Wluminosity
                    return Wluminosity

###### SUNRISE #####                
                elif W2THCL == 'WSunriseRED':
                    WSunriseRED = f.read().split('\n')[10]
                    print "## Read Weedle WSunriseRED:" + WSunriseRED
                    return WSunriseRED
                
                elif W2THCL == 'WSunriseBLUE':
                    WSunriseBLUE = f.read().split('\n')[11]
                    print "## Read Weedle WSunriseBLUE:" + WSunriseBLUE
                    return WSunriseBLUE
                
                elif W2THCL == 'WSunriseWHITE':
                    WSunriseWHITE = f.read().split('\n')[12]
                    print "##  Read Weedle WSunriseWHITE:" + WSunriseWHITE
                    return WSunriseWHITE
##### SUNSET  ######                
                elif W2THCL == 'WSunsetRED':
                    WSunsetRED = f.read().split('\n')[13]
                    print "##  Read Weedle WSunsetRED:" + WSunsetRED
                    return WSunsetRED

                elif W2THCL == 'WSunsetBLUE':
                    WSunsetBLUE = f.read().split('\n')[14]
                    print "##  Read Weedle WSunsetBLUE:" + WSunsetBLUE
                    return WSunsetBLUE
                
                elif W2THCL == 'WSunsetWHITE':
                    WSunsetWHITE = f.read().split('\n')[15]
                    print "## Read Weedle WSunsetWHITE:" + WSunsetWHITE
                    return WSunsetWHITE

                else:
                    return "##### ALERT W2THCL request Incorrect"
        else:
            sys.exit("ERROR: Please make sure you have a file called weedleAdjustment.config in %s" % currentDir)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

if __name__ == '__main__':             # Program start from here
    try:
        print readweedleClimate("WCO2")
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
