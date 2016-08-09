import mysql.connector
import toastutil
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES
from roles import SORT_ORDERS
import random

from collections import Counter
from collections import defaultdict
from heapq import *

def days_since_role(who, asof, role_names):
  where_clause = ' OR '.join([ '{} = {}'.format(role, who) for role in role_names ])
  query = 'SELECT dayof FROM future_meetings WHERE {} '.format(where_clause) \
            + 'AND dayof < "{}" ORDER BY dayof DESC'.format(asof)
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  if rows:
    return (date.today() - rows[0][0]).days 
  query = 'SELECT dayof FROM known_meetings WHERE {} ORDER BY dayof DESC'.format(where_clause)
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  return (date.today() - rows[0][0]).days if rows else 365

def absent_on_day(dayof):
  query = 'SELECT who FROM absent WHERE dayof = "{}"'.format(str(dayof))
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  return { int(row[0]) for row in rows }

def schedule_meeting(dayof):
  print "Scheduling for {}...".format(dayof)
  query = 'SELECT id FROM members'  
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  absent = absent_on_day(dayof)
  print "Absent: {!s}".format(absent)
  ids = filter(lambda who: who not in absent, [int(row[0]) for row in rows])
  cursor.close()
  used_up = set()
  schedule = {} 

  skipped_roles = [ 'momenttm' ]
  speakers = [ 'speaker1', 'speaker2', 'speaker3' ]   
  evals = [ 'eval1', 'eval2', 'eval3' ]   

  for role in SORT_ORDERS[random.randint(0, 2)]:
    if role in skipped_roles:
      continue 
    pq = []
    eligible = filter(lambda who: (who not in used_up) and \
                        toastutil.has_prereqs(who, role, dayof), ids)
    role_names = None
    if role in speakers:
      role_names = speakers
    elif role in evals:
      role_names = evals
    else:
      role_names = [ role ]
    for who in eligible:
      priority = 365 - days_since_role(who, dayof, role_names)
      heappush(pq, (priority, who))  
    schedule[role] = heappop(pq)[1]
    used_up.add(schedule[role])

  active_roles = schedule.keys()
  update = 'INSERT INTO future_meetings '                           \
    + '(dayof, {}) '.format(', '.join(active_roles))                \
    + 'VALUES ("{}", {})'.format(str(dayof),                        \
       ', '.join(['%({})s'.format(role) for role in active_roles]))
  cursor = cnx.cursor()
  cursor.execute(update, schedule)
  cnx.commit()
  cursor.close()
  toastutil.print_meeting(dayof)
  print

cnx = mysql.connector.connect(                  \
    user='tm', password='dhmtks52',             \
    host='localhost', database='toastmasters')

from_day = date.today() + timedelta(days=(7 - date.today().weekday()))
query = 'SELECT dayof FROM future_meetings ORDER BY dayof DESC'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
cursor.close()
if rows:
  from_day = rows[0][0]
query = 'SELECT dayof FROM known_meetings ORDER BY dayof DESC'
cursor = cnx.cursor()
cursor.execute(query) 
rows = cursor.fetchall()
cursor.close()
if rows and rows[0][0] >= from_day:
  from_day = rows[0][0] + timedelta(days=7)
num = int(raw_input("How many meetings to schedule starting from {}? ".format(str(from_day))))

for i in range(num):
  schedule_meeting(from_day)
  from_day = from_day + timedelta(days=7)

cnx.close()
