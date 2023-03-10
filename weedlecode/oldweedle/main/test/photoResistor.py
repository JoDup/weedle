#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

LedPin = 16
threshold = 120

def init():
	ADC0832.setup()
        GPIO.setup(LedPin, GPIO.OUT)
		
def loop():
	while True:
		res = ADC0832.getResult(0)
		print 'res = %d' % res
                if(res > threshold):
                    print 'It is night, light on...'
                    GPIO.output(LedPin, GPIO.HIGH)
                else:
                    print 'It is already dawn, light off'
                    GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.2)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print 'The end !'
