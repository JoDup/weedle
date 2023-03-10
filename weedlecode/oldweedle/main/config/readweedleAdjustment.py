import RPi.GPIO as GPIO
import time
import math
import os
import sys


def readweedleAdjustment(THCL2WAS):

    print (" == IN READ WEEDLE ADJUSTMENT == ")
    try:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        weedleAdjustConfigFile = currentDir + "/" + "weedleAdjustment.config"
        
        if os.path.isfile( weedleAdjustConfigFile ):
            with open(weedleAdjustConfigFile, "r") as f:
#### TEMPERATURE #####                
                if THCL2WAS == 'TWater':
                    TWater = f.read().split('\n')[0]
                    print "##  Read Weedle TWater:" + TWater
                    return TWater
                
                elif THCL2WAS == 'TAir':
                    TAir = f.read().split('\n')[1]
                    print "##  Read Weedle TAir:" + TAir
                    return TAir
                
                elif THCL2WAS == 'TSun':
                    TSun = f.read().split('\n')[2]
                    print "## Read Weedle TSun:" + TSun
                    return TSun
                
                elif THCL2WAS == 'Twater':
                    Twater = f.read().split('\n')[3]
                    print "##  Read Weedle Twater:" + Twater
                    return Twater
                
                elif THCL2WAS == 'Tair':
                    Tair = f.read().split('\n')[4]
                    print "##  Read Weedle Tair:" + Tair
                    return Tair
                
                elif THCL2WAS == 'Tsun':
                    Tsun = f.read().split('\n')[5]
                    print "##  Read Weedle Tsun:" + Tsun
                    return Tsun

#### HUMIDITY AIR #####
                elif THCL2WAS == 'HAWater':
                    HAWater = f.read().split('\n')[6]
                    print "##  Read Weedle HAWater:" + HAWater
                    return HAWater
                
                elif THCL2WAS == 'HAAir':
                    HAAir = f.read().split('\n')[7]
                    print "##  Read Weedle HAAir:" + HAAir
                    return HAAir
                
                elif THCL2WAS == 'HASun':
                    HASun = f.read().split('\n')[8]
                    print "##  Read Weedle HASun:" + HASun
                    return HASun
                
                elif THCL2WAS == 'HAwater':
                    HAwater = f.read().split('\n')[9]
                    print "##  Read Weedle HAwater:" + HAwater
                    return HAwater
                
                elif THCL2WAS == 'HAair':
                    HAair = f.read().split('\n')[10]
                    print "## Read Weedle HAair:" + HAair
                    return HAair
                
                elif THCL2WAS == 'HAsun':
                    HAsun = f.read().split('\n')[11]
                    print "##  Read Weedle HAsun:" + HAsun
                    return HAsun

#### HUMIDITY SOIL #####
                elif THCL2WAS == 'HSWater':
                    HSWater = f.read().split('\n')[12]
                    print "##  Read Weedle HSWater:" + HSWater
                    return HSWater
                
                elif THCL2WAS == 'HSAir':
                    HSAir = f.read().split('\n')[13]
                    print "##  Read Weedle HSAir:" + HSAir
                    return HSAir
                
                elif THCL2WAS == 'HSSun':
                    HSSun = f.read().split('\n')[14]
                    print "##  Read Weedle HSSun:" + HSSun
                    return HSSun
                
                elif THCL2WAS == 'HSwater':
                    HSwater = f.read().split('\n')[15]
                    print "##  Read Weedle HSwater:" + HSwater
                    return HSwater
                
                elif THCL2WAS == 'HSair':
                    HSair = f.read().split('\n')[16]
                    print "## Read Weedle HSair:" + HSair
                    return HSair
                
                elif THCL2WAS == 'HSsun':
                    HSsun = f.read().split('\n')[17]
                    print "##  Read Weedle HSsun:" + HSsun
                    return HSsun


#### CO2  #####
                elif THCL2WAS == 'CWater':
                    CWater = f.read().split('\n')[18]
                    print "##  Read Weedle CWater:" + CWater
                    return CWater
                
                elif THCL2WAS == 'CAir':
                    CAir = f.read().split('\n')[19]
                    print "##  Read Weedle CAir:" + CAir
                    return CAir
                
                elif THCL2WAS == 'CSun':
                    CSun = f.read().split('\n')[20]
                    print "##  Read Weedle CSun:" + CSun
                    return CSun
                
                elif THCL2WAS == 'Cwater':
                    Cwater = f.read().split('\n')[21]
                    print "##  Read Weedle Cwater:" + Cwater
                    return Cwater
                
                elif THCL2WAS == 'Cair':
                    Cair = f.read().split('\n')[22]
                    print "##  Read Weedle Cair:" + Cair
                    return Cair
                
                elif THCL2WAS == 'Csun':
                    Csun = f.read().split('\n')[23]
                    print "##  Read Weedle Csun:" + Csun
                    return Csun

#### LUMINOSITY  #####
                elif THCL2WAS == 'LWater':
                    LWater = f.read().split('\n')[24]
                    print "##  Read Weedle LWater:" + LWater
                    return LWater
                
                elif THCL2WAS == 'LAir':
                    LAir = f.read().split('\n')[25]
                    print "##  Read Weedle LAir:" + LAir
                    return LAir
                
                elif THCL2WAS == 'LSun':
                    LSun = f.read().split('\n')[26]
                    print "##  Read Weedle LSun:" + LSun
                    return LSun
                
                if THCL2WAS == 'Lwater':
                    Lwater = f.read().split('\n')[27]
                    print "##  Read Weedle Lwater:" + Lwater
                    return Lwater
                
                elif THCL2WAS == 'Lair':
                    Lair = f.read().split('\n')[28]
                    print "##  Read Weedle Lair:" + Lair
                    return Lair
                
                elif THCL2WAS == 'Lsun':
                    Lsun = f.read().split('\n')[29]
                    print "##  Read Weedle Lsun:" + Lsun
                    return Lsun
                else:
                    return "##### ALERT  TWAS request Incorrect"
        else:
            sys.exit("ERROR: Please make sure you have a file called weedleAdjustment.config in %s" % currentDir)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

if __name__ == '__main__':             # Program start from here
    try:
        print readweedleAdjustment("Tsun")
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
