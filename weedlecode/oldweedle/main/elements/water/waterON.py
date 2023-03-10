#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
#Water
RelayWater = 33

def action():
    try:
        
        print ('##### IN WATER ON ####')
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setwarnings(False)
        GPIO.setup(RelayWater, GPIO.OUT)
        print 'Water ON...'
        GPIO.output(RelayWater, GPIO.HIGH)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
        
  
def destroy():
    GPIO.output(RelayWater, GPIO.LOW)

if __name__ == '__main__':             # Program start from here
    try:
        action()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
