#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
#Water
RelayPinBlueLight = 37

def action():
    try:
        
        print ('##### IN BLUE LIGHT ON ####')
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setwarnings(False)
        GPIO.setup(RelayPinBlueLight, GPIO.OUT)
        print 'Blue Light ON...'
        GPIO.output(RelayPinBlueLight, GPIO.HIGH)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
        
  
def destroy():
    GPIO.output(RelayPinBlueLight, GPIO.LOW)

if __name__ == '__main__':             # Program start from here
    try:
        action()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

