#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

LedPin = 16
threshold = 120
        
def readLuminosity():
    try:
        print ("== IN READ LUMINOSITY IN THE BOX == ")
        luminosity = -100
        ADC0832.setup()
        GPIO.setup(16, GPIO.OUT)
        luminosity = ADC0832.getResult(0)
        print '## luminosity = %d' % luminosity
        GPIO.output(16, GPIO.HIGH)
        return luminosity
       

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource
            return -100


if __name__ == '__main__':
    try:
        readLuminosity()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print 'The end !'
