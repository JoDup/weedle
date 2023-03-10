#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import sys

#Hot Air
RelayHotAir = 31

def action():
    try:
        
        print ('##### IN SUN ON ####')
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setwarnings(False)
        GPIO.setup(RelayHotAir, GPIO.OUT)
        print 'Hot Air ON...'
        GPIO.output(RelayHotAir, GPIO.HIGH)
        #GPIO.cleanup()                     # Release resource

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
   
  
def destroy():
    GPIO.output(RelayHotAir, GPIO.LOW)

if __name__ == '__main__':             # Program start from here
    try:
        action()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()


