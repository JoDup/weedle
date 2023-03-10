import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

def RCtime(RCpin):
    lecture=0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while GPIO.input(RCpin) == GPIO.LOW:
        lecture += 1
        time.sleep(0.01)
    return lecture


while 1:
    try:
    # Violet et GRIS sur sensor    
        moisture = RCtime(23)
    #    moisture = RCtime(24)
    #    moisture = RCtime(25)
    #    moisture = RCtime(8)
        print moisture
        time.sleep(1)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
