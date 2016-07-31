import mysql.connector, csv, sys
from roles import SQL_MEETING_ROLES

cnx = mysql.connector.connect(                  \
    user='tm', password='dhmtks52',             \
    host='localhost', database='toastmasters')

with open(sys.argv[1], 'rb') as csvfile:
  reader = csv.reader(csvfile, dialect='excel')

  for line in reader:
    active_roles = zip(*filter(lambda (i, role): line[i + 1] != 'None', \
                               enumerate(SQL_MEETING_ROLES)))[1]  
    to_insert = {}
    for role in active_roles:
      to_insert[role] = int(line[1 + SQL_MEETING_ROLES.index(role)])
    
    update = 'INSERT INTO known_meetings ' \
      + '(dayof, {}) '.format(', '.join(active_roles)) \
      + 'VALUES ("{}", {})'.format(line[0], \
         ', '.join(['%({})s'.format(role) for role in active_roles]))
    cursor = cnx.cursor()
    cursor.execute(update, to_insert)
    cnx.commit()
    cursor.close()

cnx.close()
