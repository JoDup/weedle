#!/usr/bin/env python

import os
import sys
import time

import sqlite3

from util.weedleRunActivity import weedleRunActivity
from util.weedleRecommendation import weedleRecommendation
from util.weedleScheduler import maintainWeedleSchedule


def init():

    # Connect to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    
    #get the plant to manage
    cursor = conn.execute("SELECT * FROM W_WEEDLE_PLANT ")
    for row in cursor:
        ## For each plant do the job
        plantSize=row[2]
        
        #first run the recommendation
        weedleRecommendation(conn,plantSize)
                
        garden = conn.execute("SELECT * FROM W_WEEDLE_GARDEN WHERE DEVICE_TYPE='CONTROL'")
        for row in garden:
           ## For each plant do the job
           activity=row[1]
           #second run the schedule calculation for each element
           maintainWeedleSchedule(conn,plantSize,activity)
           #third execute on the activity
           weedleRunActivity(conn,plantSize,activity)
    
    conn.commit()
    conn.close()

        
if __name__ == '__main__':
    init()
