#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarning(False)          # Numbers GPIOs by physical location
    GPIO.setup(Relay1Pin, GPIO.OUT)
    GPIO.setup(Relay2Pin, GPIO.OUT)
    GPIO.setup(Relay3Pin, GPIO.OUT)
    GPIO.setup(Relay4Pin, GPIO.OUT)
    GPIO.setup(Relay5Pin, GPIO.OUT)
    GPIO.setup(Relay6Pin, GPIO.OUT)

def loop():
    while True:
        print 'relay off...'
        GPIO.output(Relay1Pin, GPIO.LOW)
        GPIO.output(Relay2Pin, GPIO.LOW)
        GPIO.output(Relay3Pin, GPIO.LOW)
        GPIO.output(Relay4Pin, GPIO.LOW)
        GPIO.output(Relay5Pin, GPIO.LOW)
        GPIO.output(Relay6Pin, GPIO.LOW)
        time.sleep(5)
        print '...relayd on'
        GPIO.output(Relay1Pin, GPIO.HIGH)
        GPIO.output(Relay2Pin, GPIO.HIGH)
        GPIO.output(Relay3Pin, GPIO.HIGH)
        GPIO.output(Relay4Pin, GPIO.HIGH)
        GPIO.output(Relay5Pin, GPIO.HIGH)
        GPIO.output(Relay6Pin, GPIO.HIGH)
        time.sleep(10)
 
def destroy():
    GPIO.output(RelayPin, GPIO.LOW)
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':             # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

