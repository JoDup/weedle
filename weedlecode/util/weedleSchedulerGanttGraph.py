import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# Define the tasks and their start/end dates
tasks = [
    ('Task 1', dt.datetime(2023, 3, 1, 8, 0), dt.datetime(2023, 3, 1, 12, 0)),
    ('Task 2', dt.datetime(2023, 3, 1, 12, 0), dt.datetime(2023, 3, 1, 16, 0)),
    ('Task 3', dt.datetime(2023, 3, 1, 16, 0), dt.datetime(2023, 3, 2, 8, 0)),
    ('Task 4', dt.datetime(2023, 3, 2, 8, 0), dt.datetime(2023, 3, 3, 16, 0))
]
# Sort the tasks by end time in descending order
tasks.sort(key=lambda x: x[2], reverse=True)

# Create a figure and set its size
fig = plt.figure(figsize=(10, 5))

# Create the Gantt chart
ax = fig.add_subplot(111)
for i in range(len(tasks)):
    task = tasks[i]
    start_time = mdates.date2num(task[1])
    end_time = mdates.date2num(task[2])
    duration_hours = (end_time - start_time) * 24
    if i == 1:
        ax.broken_barh([(start_time, duration_hours)], (i, 1), facecolors=('tab:red'))
    else:
        ax.broken_barh([(start_time, duration_hours)], (i, 1), facecolors=('tab:blue'))
    ax.text(start_time+(end_time-start_time)/2, i+0.5, task[0], ha='center', va='center', color='white')

# Set the labels and ticks
ax.set_ylim(0, len(tasks))
ax.set_xlim(mdates.date2num(dt.datetime(2023, 3, 1, 8, 0)), mdates.date2num(dt.datetime(2023, 3, 3, 16, 0)))
ax.set_xlabel('Time')
ax.set_yticks([i+0.5 for i in range(len(tasks))])
ax.set_yticklabels([task[0] for task in tasks])

# Format the x-axis as dates
xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Show the chart
plt.show()
