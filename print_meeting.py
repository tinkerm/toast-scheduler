import mysql.connector
from roles import SQL_MEETING_ROLES
import menus


cnx = mysql.connector.connect(user='tm', password='dhmtks52', host='localhost', database='toastmasters')

query = 'SELECT dayof FROM known_meetings ORDER BY dayof'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
choices = [ row[0] for row in rows ]

choice = menus.get_choice(choices)
chosen_one = str(choices[choice])

print "--> " + chosen_one
print

for role in SQL_MEETING_ROLES:
  query = 'SELECT fname, lname, title, dayof, id, {0} FROM known_meetings INNER JOIN members ON id = {0} WHERE dayof = "{1}"'.format(role, chosen_one)
  cursor = cnx.cursor()
  cursor.execute(query)
  rows = cursor.fetchall()
  if rows:
    print "{}: {} {}, {}".format(role, rows[0][0], rows[0][1], rows[0][2])
  else:
    print "{}: ---".format(role)
  cursor.close()

cnx.close()

