import mysql.connector
import menus
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

cnx = mysql.connector.connect(                  \
    user='tm', password='dhmtks52',             \
    host='localhost', database='toastmasters')

earliest_possible = date.today() + timedelta(days=(7 - date.today().weekday()))

choices = [ earliest_possible + timedelta(days=n) for n in range(-7, 8 * 7, 7) ]

choice = menus.get_choice(choices)
dayof = str(choices[choice])

end_choices = [ choices[choice] + timedelta(days=n) for n in range(0, 24 * 7, 7) ]
end_choice = menus.get_choice(end_choices)
lastdayof = str(end_choices[end_choice])

print "Who will be absent from {} to {}?".format(dayof, lastdayof)

who = menus.choose_member()

if who is not None:
  day = choices[choice]
  while day <= end_choices[end_choice]:
    update = 'INSERT INTO absent ' \
      + '(who, dayof) VALUES ("{}", "{}")'.format(who, str(day))
    cursor = cnx.cursor()
    cursor.execute(update)
    cnx.commit()
    cursor.close()
    day += timedelta(days=7)
  
cnx.close()
