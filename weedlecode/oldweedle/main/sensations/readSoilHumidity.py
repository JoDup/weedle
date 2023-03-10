#!/usr/bin/python

import spidev
import time
import os
import sys

import RPi.GPIO as GPIO

hs40 =  -100
hs55 =  -100
hs70 =  -100
hs85 =  -100


# Function to read SPI data from MCP3008 chip
def readSoilHumdity40():
     try:
        print ("== IN READ SOIL HUMIDITY 40 IN THE BOX == ")
        lecture=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(8, GPIO.OUT)
        GPIO.output(8, GPIO.LOW)
        time.sleep(0.5)
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(8) == GPIO.LOW:
            lecture = 40
        GPIO.cleanup()            
        return lecture

     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource
            return -100
    

def readSoilHumdity55():
    try:
        print ("== IN READ SOIL HUMIDITY 55 IN THE BOX == ")
        lecture=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.5)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(23) == GPIO.LOW:
            lecture = 55
        GPIO.cleanup()            
        return lecture

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource
            return -100
    
def readSoilHumdity70():
    try:
        print ("== IN READ SOIL HUMIDITY 70 IN THE BOX == ")
        lecture=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, GPIO.LOW)
        time.sleep(0.5)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(24) == GPIO.LOW:
            lecture = 70
        GPIO.cleanup()            
        return lecture

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource
            return -100

def readSoilHumdity85():
     try:
        print ("== IN READ SOIL HUMIDITY 85 IN THE BOX == ")
        lecture=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(25, GPIO.OUT)
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.5)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(25) == GPIO.LOW:
            lecture = 85
        GPIO.cleanup()            
        return lecture

     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource
            return -100

def destroy(pin):
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()                     # Release resource


if __name__ == '__main__':             # Program start from here
    try:
        while True:
            hs40 =  readSoilHumdity40()
            hs55 =  readSoilHumdity55()
            hs70 =  readSoilHumdity70()
            hs85 =  readSoilHumdity85()
            
            print ("hs40: " + str(hs40)
                 +" hs55: " + str(hs55)
                 +" hs70: " + str(hs70)
                 +" hs85: " + str(hs85)
                 + "  " )
            time.sleep(5)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy(25)

