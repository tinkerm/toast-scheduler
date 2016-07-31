import menus, toastutil
import mysql.connector
from datetime import date, timedelta

cnx = mysql.connector.connect(                  \
    user='tm', password='dhmtks52',             \
    host='localhost', database='toastmasters')

query = 'SELECT dayof FROM future_meetings ORDER BY dayof ASC'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
cursor.close()
if rows:
  days = [ row[0] for row in rows ]
  choice = menus.get_choice([ str(day) for day in days ])
  n = int(raw_input("How many meetings to include in the forecast? "))
  toastutil.latex_forecast(days[choice], n)
