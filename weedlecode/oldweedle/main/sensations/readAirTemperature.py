#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import sys

def readAirTemperature():
    
    try:
        
        AirTemperature = 5
        THdata = []
        data = []
        
        print ("== IN READ AIR TEMPERATURE IN THE BOX == ")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        time.sleep(2)
        GPIO.setup(AirTemperature, GPIO.OUT)
        GPIO.output(AirTemperature, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(AirTemperature, GPIO.HIGH)
        GPIO.setup(AirTemperature, GPIO.IN)
        while GPIO.input(AirTemperature) == GPIO.LOW:
            continue
        while GPIO.input(AirTemperature) == GPIO.HIGH:
            continue
        j = 0
        while j < 40:
            k = 0
            while GPIO.input(AirTemperature) == GPIO.LOW:
                continue
            while GPIO.input(AirTemperature) == GPIO.HIGH:
                k += 1
                if k > 100:
                    break
            if k < 8:
                data.append(0)
            else:
                data.append(1)
            j += 1

        # print("sensor is working.")
        # print(data)
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0
        for i in range(8):
            humidity += humidity_bit[i] * 2 ** (7 - i)
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
            temperature += temperature_bit[i] * 2 ** (7 - i)
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
            check += check_bit[i] * 2 ** (7 - i)
            tmp = humidity + humidity_point + temperature + temperature_point
        if check == tmp:
            print "## temperature:%d.%d" %(temperature,temperature_point),"C"," humidity :", humidity, "%"
            #airtemperature = str(temperature)+"."+str(temperature_point)
            airtemperature = temperature
            return (airtemperature)
        else:
            # print("wrong")
            time.sleep(1)
            return -100

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()                     # Release resource

def destroy(pin):
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()                     # Release resource


if __name__ == '__main__':             # Program start from here
    try:
        temp = readAirTemperature()
        print ("temp: " + str(temp))
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy(5)

