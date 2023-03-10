#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import sys


def readAirHumidity():
        try:

            airHumidity = 5
            THdata = []
            data = []
            print ("== IN READ AIR HUMIDITY IN THE BOX == ")
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            time.sleep(2)
            GPIO.setup(airHumidity, GPIO.OUT)
            GPIO.output(airHumidity, GPIO.LOW)
            time.sleep(0.02)
            GPIO.output(airHumidity, GPIO.HIGH)
            GPIO.setup(airHumidity, GPIO.IN)
            while GPIO.input(airHumidity) == GPIO.LOW:
                continue
            while GPIO.input(airHumidity) == GPIO.HIGH:
                continue
            j = 0
            while j < 40:
                k = 0
                while GPIO.input(airHumidity) == GPIO.LOW:
                    continue
                while GPIO.input(airHumidity) == GPIO.HIGH:
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
            
            GPIO.cleanup() 
            
            if check == tmp:
                print "##  temperature:%d.%d" %(temperature,temperature_point),"C"," humidity :", humidity, "%"
                #airHumdity = str(temperature)+"."+str(temperature_point)
                airHumdity = humidity
                return (airHumdity)
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
        airHumidity = readAirHumidity()
        print ("temp: " + str(airHumidity))
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy(5)


