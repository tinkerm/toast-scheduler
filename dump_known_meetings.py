import mysql.connector
import menus
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

cnx = mysql.connector.connect(user='tm', password='dhmtks52', host='localhost', database='toastmasters')

query = 'SELECT dayof, {} FROM known_meetings ORDER BY dayof'.format(', '.join(SQL_MEETING_ROLES))
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
for row in rows:
  print ','.join([str(thing) for thing in row])
cnx.close()
