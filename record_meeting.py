import mysql.connector
import menus
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
dars = [ date(*[int(piece) for piece in row[0].split('-')]) for row in rows ]
for this_day in dars:
  if this_day == earliest_possible:
    earliest_possible = earliest_possible + timedelta(days=7) 

choices = [ ]

cur_day = earliest_possible
while cur_day <= date.today():
  if cur_day not in dars:
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

print to_insert

cnx.close()
