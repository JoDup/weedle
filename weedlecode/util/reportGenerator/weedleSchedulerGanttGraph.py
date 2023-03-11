import sqlite3
import datetime as dt
import random
import os.path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.ticker import FuncFormatter

from datetime import date

# Define a function to format the x-axis labels
def format_hour(x, pos):
    # Convert the numeric value to a datetime object
    date = dt.datetime.fromtimestamp(x)
    # Format the label as DAY-HOUR
    label = date.strftime('%d-%H')
    return label

def createSchedulerGanttGraph():

    currentTime = dt.datetime.now()
    currentDay = date.today()    

    # Establish a connection to the database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')

    # Create a cursor object
    cur = conn.cursor()

    # Execute the SELECT statement to retrieve tasks data from a table named 'tasks_table'
    cur.execute("SELECT task_name, start_time, end_time from weedle_gantt")

    tasks = cur.fetchall()[::-1]

    # Set up the plot
    fig, ax = plt.subplots()

    # Set the y-axis limit
    ax.set_ylim(0, len(tasks))

    # Define a list of colors to choose from
    #colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'brown', 'gray']

    # Set the x-axis locator and formatter
    locator = mdates.HourLocator(interval=1)
    formatter = mdates.DateFormatter('%H:%M')

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # Set the x-axis formatter to the format_hour function

    # Loop through the tasks and plot them on the Gantt chart
    for i, task in enumerate(tasks):
        task_name = task[0]
        start_time = dt.datetime.strptime(task[1], '%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.strptime(task[2], '%Y-%m-%d %H:%M:%S')
        duration = end_time - start_time
    
        print('DEBUG task_name '+task_name+' start_time '+str(start_time)+' end_time '+str(end_time)+' Duration '+str(duration))
        # Generate a random color for each task
        if 'SUN' in task_name:
            color = 'orange'
        if 'WATER' in task_name:
            color = 'blue'
        if 'AIR' in task_name:
            color = 'pink'
        if 'HOTAIR' in task_name:
            color = 'red'

        # Plot the task as a horizontal bar with the chosen color
        ax.broken_barh([(start_time, duration)], (i, 1), label=task_name, color=color)

    #ax.xaxis.set_major_formatter(FuncFormatter(format_hour))

    # Set the chart title and axis labels
    ax.set_title('Weedle Scheduler')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Activity')

    # Add a legend to the chart
    ax.legend()


    filename = 'weedleScheduler'+str(currentDay)+'.png'
    filepath = '/home/weedle/weedlecode/weedleReport/' + filename

    # Check if file already exists
    if os.path.isfile(filepath):
       os.remove(filepath)
    # display plot
    #plt.show()
    # Save the graph as a PNG file
    plt.savefig(filepath)

    # Close the cursor and connection
    cur.close()
    conn.close()


