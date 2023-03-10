#!/usr/bin/env python

import os
import sys
import time
from util.runElement import runElement
from util.recommendation import recommendation

water = 0
air = 1
sun = 2
plantSize='SMALL'

def runRecommendation():
    recommendation(plantSize)

def runAllElement():
    runElement(plantSize,'SUN',sun)
    runElement(plantSize,'AIR',air)
    runElement(plantSize,'WATER',water)

if __name__ == '__main__':
    try:
       runRecommendation()
    except Exception as e:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print('##########################')
        print('### RECOMMENDATION FAILED')
        print('### with issue ',e)	
        print('##########################')
        print('                          ')
        print('                          ')
    finally:
        runAllElement()
