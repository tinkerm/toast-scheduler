import mysql.connector
import menus
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

cnx = mysql.connector.connect(                  \
    user='tm', password='dhmtks52',             \
    host='localhost', database='toastmasters')

earliest_possible = date.today() + timedelta(days=(7 - date.today().weekday()))

choices = [ earliest_possible + timedelta(days=n) for n in range(0, 8 * 7, 7) ]

choice = menus.get_choice(choices)
dayof = str(choices[choice])

print "Who will be absent on {}?".format(dayof)

who = menus.choose_member()

if who is not None:
  update = 'INSERT INTO absent ' \
    + '(who, dayof) VALUES ("{}", "{}")'.format(who, dayof)
  cursor = cnx.cursor()
  cursor.execute(update)
  cnx.commit()
  cursor.close()
  
cnx.close()
