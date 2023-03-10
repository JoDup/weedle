#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

channel = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#def init():
#     print "Initial state = %d" % (GPIO.input(channel))
#    GPIO.add_event_detect(channel, GPIO.BOTH)
#    GPIO.add_event_callback(channel, callback)

#def loop():
#    while True:
#        time.sleep(1)

def callback(channel):
        if GPIO.input(channel):
                print "Water Detected"
        else:
                print "No Water Detected"

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
       time.sleep(1)

#if __name__ == '__main__':
#    init()
#    try:
#        loop()
#    except KeyboardInterrupt: 
#        print 'The end !'
