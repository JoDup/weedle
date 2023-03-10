import RPi.GPIO as GPIO
import time
import math
import os
import sys
sys.path.insert(0,'/home/pi/weedle/gardener/main')


import elements.water.waterON
import elements.water.waterOFF
import elements.air.hotairON
import elements.air.hotairOFF
import elements.air.airON
import elements.air.airOFF
import config.readweedleClimate
import config.readweedleAdjustment
import sensations.readAirTemperature

water = "0"
air = "0"
sun = "0"

def applyWater(waterSec):
### APPLY WATER
    try:
            if waterSec > 20:
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                print "\/\/\/\/\/\/\/\/    BRAIN    /\/\/\/\/\/\/\/\/\/"
                print "####  ALERT TIME ADJUSTMENT TO HIGH TO USE WATER "
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                waterSec = 1
            
            print "## Turn ON WATER for: " + str(waterSec)
            elements.water.waterON.action()
            time.sleep(int(waterSec))
            print "## Turn OFF WATER"
            elements.water.waterOFF.action()
            
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()


def applyAir(airSec):
### APPLY AIR
    try:
            if airSec > 140:
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                print "\/\/\/\/\/\/\/\/    BRAIN    /\/\/\/\/\/\/\/\/\/"
                print "#### ALERT TIME ADJUSTMENT TO HIGH TO USE via AIR "
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                airSec = 1
                
            print "## Turn ON AIR for: " + str(airSec)
            elements.air.airON.action()
            time.sleep(int(airSec))
            print "## Turn OFF AIR"
            elements.air.airOFF.action()

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

def applySun(sunSec):
### APPLY Sun
    try:
            if sunSec > 140:
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                print "\/\/\/\/\/\/\/\/    BRAIN    /\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                print "#### ALERT TIME ADJUSTMENT TO HIGH TO USE via SUN - HOTAIR"
                print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
                sunSec = 1
            
            print "##  Turn ON SUN - HOT AIR for: " + str(sunSec)
            elements.air.hotairON.action()
            time.sleep(int(sunSec))
            print "##  Turn OFF SUN - HOT AIR"
            elements.air.hotairOFF.action()

### LOG THE ACTIONSSS
            
    
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
