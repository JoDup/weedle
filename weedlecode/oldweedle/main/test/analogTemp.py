#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time
import math

LedPin = 16
threshold = 200
def init():
	ADC0832.setup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LedPin, GPIO.OUT)
        GPIO.output(LedPin, GPIO.LOW)

def loop():
	while True:
		analogVal = ADC0832.getResult(0)
                print 'analogVal = %d' % analogVal
                if(analogVal < threshold):
                    GPIO.output(LedPin, True)
                else:
                    GPIO.output(LedPin, False)
                
		time.sleep(0.2)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print 'The end !'
