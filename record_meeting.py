import mysql.connector
import menus, toastutil
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

from collections import Counter
from collections import defaultdict

cnx = mysql.connector.connect(user='tm', password='dhmtks52', host='localhost', database='toastmasters')

earliest_possible = date(2016, 6, 6)
query = 'SELECT dayof FROM known_meetings ORDER BY dayof'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
dars = [ row[0] for row in rows ]
for this_day in dars:
  if this_day == earliest_possible:
    earliest_possible = earliest_possible + timedelta(days=7) 

choices = [ ]

cur_day = earliest_possible
while cur_day <= date.today() + timedelta(days=7):
  if cur_day not in dars and not toastutil.is_holiday(cur_day):
    choices.append(cur_day)  
  cur_day = cur_day + timedelta(days=7)  

choice = menus.get_choice(choices)
chosen_one = str(choices[choice])

print "--> " + chosen_one
print "--> Will now prompt for meeting roles."
print


query = 'SELECT id, fname, lname, title FROM members'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
names = [' '.join(row[1:]) for row in rows ]
ids = [int(row[0]) for row in rows ]

to_insert = {}

for role in SQL_MEETING_ROLES:
  print "------------------- {} on {} ------------------".format(role.upper(), chosen_one)
  choice = menus.get_choice(names)
  if choice is not None:
    to_insert[role] = ids[choice]

active_roles = to_insert.keys()
update = 'INSERT INTO known_meetings '                                                                            \
  + '(dayof, {}) '.format(', '.join(active_roles))                                                           \
  + 'VALUES ("{}", {})'.format(str(chosen_one), ', '.join(['%({})s'.format(role) for role in active_roles]))
cursor = cnx.cursor()
cursor.execute(update, to_insert)
cnx.commit()
cursor.close()

print "Validation: "
print "------------"
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
