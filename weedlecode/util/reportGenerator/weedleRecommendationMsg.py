import sqlite3

from datetime import date, timedelta

def weedleRecommendation():
    
    currentDay = date.today()
    # Calculate yesterday's date
    yesterday = currentDay - timedelta(days=1)

    # Connect to SQLite database
    conn = sqlite3.connect('/home/weedle/weedlecode/db/weedle.db')
    cursor = conn.cursor()

    # Query table and retrieve data
    cursor.execute("SELECT hour, 'P'||priority||': '||recommendation FROM w_weedle_recommendation where day=? and priority <= 4 order by HOUR desc", 
                  (str(yesterday),))

    rows = cursor.fetchall()
    
    html_content = ""

    if len(rows)!=0:
       # Create the message body
       # HTML content
       html_content = """
        <table>
         <tr>
          <th>Hour</th>
          <th>Recommendation</th>
        </tr>
      """ 
#    message = "Weedle Recommendations: "+str(currentDay)+"\n\n"
       for row in rows:
           html_content += "<tr><td style='padding:50px'>"f"{row[0]}</td>" + "<td 'style=padding:50px'>"f"{row[1]}</td>" + "</tr>"

       html_content += """
       </table>
       """

    return html_content

## MAIN CALL
#if __name__ == '__main__':
#    print(weedleRecommendation())	
