import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Query table and retrieve data
cursor.execute('/home/weedle/weedlecode/db/weedle.db')
data = cursor.fetchall()

# Create bar chart
x_values = [row[0] for row in data]
y_values = [row[1] for row in data]
plt.bar(x_values, y_values)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('My Table Graph')

# Save chart as PNG file
plt.savefig('/home/weedle/weedlecode/weedleReport/weedleRecommendation.png')

