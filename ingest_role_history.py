import mysql.connector, csv, sys

from collections import Counter
from collections import defaultdict

cnx = mysql.connector.connect(user='tm', password='dhmtks52', host='localhost', database='toastmasters')

def get_member_id(fname, lname):
  query = 'SELECT id FROM members WHERE fname = %s AND lname = %s'
  cursor = cnx.cursor()
  cursor.execute(query, (fname, lname))
  rows = cursor.fetchall()
  if len(rows) == 0:
    add_member = 'INSERT INTO members (fname, lname) VALUES (%s, %s)'
    cursor.execute(add_member, (fname, lname))
    cnx.commit()
    cursor.close()
    return get_member_id(fname, lname)    
  else:
    cursor.close()
    return rows[0][0]

translator = {                            \
  "Toastmaster"         : "toastmaster",  \
  "Speaker"             : "speaker",      \
  "Evaluator"           : "eval",         \
  "Timer"               : "timer",        \
  "Grammarian"          : "grammarian",   \
  "Vote Counter"        : "votecounter",  \
  "Ah Counter"          : "ahcounter",    \
  "Toastmaster Moment"  : "momenttm",     \
  "JokeMaster"          : "jokemaster",   \
  "Listener"            : "listener",     \
  "Topic Master"        : "topicmaster",  \
  "General Evaluator"   : "geneval"       \
}

def stripper(role):
  if role.find("Speaker #") != -1:
    return "Speaker"
  if role.find("Evaluator #") != -1:
    return "Evaluator"
  return role

with open(sys.argv[1], 'rb') as csvfile:
  reader = csv.reader(csvfile, dialect='excel')
  members = reader.next()[1:]

  tallies = { member: Counter() for member in members }

  for line in reader:
    role = translator[stripper(line[0])]
    for i, member in enumerate(members):
      tallies[member].update([role] * int(line[i + 1]))

  for member in members:
    this_member = get_member_id(*member.split(' '))
    roles, counts = zip(*tallies[member].most_common())
    cursor = cnx.cursor()
    update_role_history = ("INSERT INTO role_history"
                           "(who, {}) "
                           "VALUES ({}, {})")
    update_role_history = update_role_history.format( \
      ', '.join(roles),                               \
      this_member,                                    \
      ', '.join(['%s'] * len(counts))                 \
    )
    print "Recording history for {}...".format(member)
    cnx.commit()
    cursor.close() 

cnx.close()
  
