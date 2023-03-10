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

def init():
    runElement(plantSize,'SUN',sun)
    runElement(plantSize,'AIR',air)
    recommendation(plantSize)
        
if __name__ == '__main__':
    init()
