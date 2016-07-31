import mysql.connector
import menus
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

def print_stuff(line, i=0):
  as_text = []
  for thing in line:
    as_text.append("({}) {}".format(i, thing).ljust(32))
    i += 1
  print ''.join(as_text)    
  return i

def get_choice(choices):
  print
  walkers = [iter(choices)] * 3  
  lines, i = zip(*walkers), 0
  for line in lines:
    i = print_stuff(line, i) 
  if len(lines) * 3 < len(choices):
    i = print_stuff(choices[-(len(choices) - 3 * len(lines)):], i)  
  c = -1
  while c not in range(i):
    print 
    try: 
      raw = raw_input("Enter your choice> ")
      if len(raw) == 0:   
        return None
      c = int(raw)
    except:
      pass
  return c

def choose_member():
  cnx = mysql.connector.connect(                  \
      user='tm', password='dhmtks52',             \
      host='localhost', database='toastmasters')
  query = 'SELECT id, fname, lname, title FROM members'
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  names = [' '.join(row[1:]) for row in rows ]
  ids = [int(row[0]) for row in rows ]
  cursor.close()
  cnx.close()

  choice = menus.get_choice(names)

  return None if choice is None else ids[choice]
