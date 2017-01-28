import mysql.connector
import menus
from datetime import date, timedelta
from roles import SQL_MEETING_ROLES

precs = {                            \
  "toastmaster" : 0,\
  "speaker1" : 3,   \
  "speaker2" : 5,   \
  "speaker3" : 7,   \
  "eval1" : 4,      \
  "eval2" : 6,      \
  "eval3" : 8,      \
  "timer" : 10,     \
  "grammarian" : 11, \
  "votecounter" : 12,\
  "ahcounter" : 13,  \
  "momenttm" :  None,   \
  "jokemaster" : 14, \
  "listener" : 9,    \
  "topicmaster" : 1, \
  "geneval" : 2     \
}

names = {                            \
  "toastmaster" : 'Toastmaster',     \
  "speaker1" : '\\nth{1} Speaker',    \
  "speaker2" : '\\nth{2} Speaker',    \
  "speaker3" : '\\nth{3} Speaker',    \
  "eval1" : 'Evaluator',    \
  "eval2" : 'Evaluator',    \
  "eval3" : 'Evaluator',    \
  "timer" : 'Timer',      \
  "grammarian" : 'Grammarian',  \
  "votecounter" : 'Vote Counter', \
  "ahcounter" : 'Ah Counter',   \
  "momenttm" :  None,   \
  "jokemaster" : 'Jokemaster',  \
  "listener" : 'Listener',    \
  "topicmaster" : 'Topicmaster',  \
  "geneval" : 'Gen.\\ Eval.' \
}

def prompt_for_member():
  local_cnx = mysql.connector.connect(                  \
            user='tm', password='dhmtks52',             \
            host='localhost', database='toastmasters')
  query = 'SELECT id, fname, lname, title FROM members'
  cursor = local_cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  names = [' '.join(row[1:]) for row in rows ]
  ids = [int(row[0]) for row in rows ]
  local_cnx.close()
  return ids[menus.get_choice(names)]

def is_holiday(dayof):
  local_cnx = mysql.connector.connect(                  \
            user='tm', password='dhmtks52',             \
            host='localhost', database='toastmasters')
  query = 'SELECT * FROM holidays WHERE dayof = "{}"'.format(dayof)
  cursor = local_cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  local_cnx.close()
  return True if rows else False

def num_of_using(who, role, asof, cnx):
  query = 'SELECT {} FROM role_history WHERE who = {}'.format(role, who)
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt = int(rows[0][0]) if rows else 0

  all_roles = [ role + str(i) for i in range(1, 4) ]
  condition = ' = {} OR '.format(who)

  query = 'SELECT COUNT(*) FROM known_meetings WHERE ' \
          + condition.join(all_roles) + ' = {}'.format(who) 
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt += int(rows[0][0]) if rows else 0

  query = 'SELECT COUNT(*) FROM future_meetings WHERE (' \
          + condition.join(all_roles) + ' = {} '.format(who) \
          + ') AND dayof < "{}"'.format(asof)
    
  cursor = cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt += int(rows[0][0]) if rows else 0

  return cnt

def num_of(who, role, asof, beforeOnly = True):
  local_cnx = mysql.connector.connect(                  \
            user='tm', password='dhmtks52',             \
            host='localhost', database='toastmasters')
  query = 'SELECT {} FROM role_history WHERE who = {}'.format(role, who)
  cursor = local_cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt = int(rows[0][0]) if rows else 0
    

  all_roles = [ role + str(i) for i in range(1, 4) ]
  condition = ' = {} OR '.format(who)

  query = 'SELECT COUNT(*) FROM known_meetings WHERE ' \
          + condition.join(all_roles) + ' = {}'.format(who) 
  cursor = local_cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt += int(rows[0][0]) if rows else 0

  if beforeOnly:
    query = 'SELECT COUNT(*) FROM future_meetings WHERE (' \
            + condition.join(all_roles) + ' = {} '.format(who) \
            + ') AND dayof < "{}"'.format(asof)
  else:
    query = 'SELECT COUNT(*) FROM future_meetings WHERE (' \
            + condition.join(all_roles) + ' = {} '.format(who) \
            + ') AND dayof <= "{}"'.format(asof)
    
  cursor = local_cnx.cursor()
  cursor.execute(query) 
  rows = cursor.fetchall()
  cursor.close()
  cnt += int(rows[0][0]) if rows else 0

  local_cnx.close()
  
  return cnt

def has_prereqs(who, role, asof):
  if role in ['eval1', 'eval2', 'eval3']:
    return num_of(who, 'speaker', asof) >= 3
  elif role == 'geneval':
    return num_of(who, 'eval', asof) >= 3
  else:
    return True

def latex_forecast(startday, numdays=8):
  local_cnx = mysql.connector.connect(                  \
            user='tm', password='dhmtks52',             \
            host='localhost', database='toastmasters')

  lastday = startday + timedelta(days=(numdays - 1) * 8)
  holiday_offsets = [] 
  query = 'SELECT (dayof) FROM holidays ' \
            + 'WHERE dayof >= "{}" AND dayof <= "{}"'.format(str(startday), str(lastday)) 
  cursor = local_cnx.cursor()
  cursor.execute(query)
  rows = cursor.fetchall()
  cursor.close()
  for row in rows:
    query = 'SELECT COUNT(*) FROM future_meetings ' \
              + 'WHERE dayof >= "{}" AND dayof < "{}"'.format(str(startday), str(row[0])) 
    cursor = local_cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    holiday_offsets.append(int(rows[0][0]))

  fout = open("schedules/forecast_from_{}.tex".format(str(startday)), "w")

  fout.write(r'\documentclass[12pt]{article}' + '\n\n')
  fout.write(r'\usepackage{geometry}' + '\n')
  fout.write(r'\usepackage{pdflscape}' + '\n')
  fout.write(r'\usepackage{adjustbox}' + '\n')
  fout.write(r'\usepackage[super]{nth}' + '\n')
  fout.write(r'\usepackage[table,svgnames]{xcolor}' + '\n')
  fout.write(r'\usepackage{tabu,booktabs}' + '\n\n')
  fout.write(r'\pagenumbering{gobble}' + '\n\n')
  fout.write(r'\begin{document}' + '\n')
  fout.write(r'  \newgeometry{margin=1cm}' + '\n')
  fout.write(r'  \begin{landscape}' + '\n')
  fout.write(r'    \begin{center}' + '\n')
  fout.write(r'      {\Large \textbf{Agenda Forecast for Plano Frontier Toastmasters}}'    \
               + '\\footnote{{As of {}.}} \\\\'.format(date.today()) + '\n')
  fout.write(r'    \end{center}' + '\n')
  fout.write(r'    \vspace{12pt}' + '\n')
  fout.write('    \\extrarowsep=7.2px \\begin{{tabu}} to \\linewidth{{{}}}\\hline\n'.format( \
              '|X[1.15]|' + 'X[c]|' * numdays)) 
  fout.write('      \\taburowcolors[2]2{Azure..white}\n') 
  fout.write(r'      & ' + ' & '.join( \
                ['\\textbf{' + (startday + timedelta(days=i*7)).strftime('%b %d') + '}' \
                    for i in range(numdays)]) + '\\\\\\hline\n')
  skipped_roles = [ 'momenttm' ] 
  the_roles = sorted([role for role in SQL_MEETING_ROLES if role not in skipped_roles ], key=lambda role: precs[role]) 
  
  for role in the_roles:
    fout.write('      \\textbf{{{}}} & '.format(names[role])) 
    query = 'SELECT fname, lname, title FROM members ' \
              + 'INNER JOIN future_meetings ON {} = id '.format(role) \
              + 'WHERE dayof >= "{}" AND dayof <= "{}" ORDER BY dayof'.format(str(startday), str(lastday)) 
    cursor = local_cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for which_holiday, offset in enumerate(holiday_offsets):
      rows.insert(offset, [ ' ', ' ' ])
    fout.write('      ' + ' & '.join([ \
      ( r'{\small ' + row[0] + ' ' + row[1][0] + r'}') for row in rows ]) + '\\\\')       
    if role == 'geneval' or role == 'eval3' or role == the_roles[-1]:
      fout.write('\\hline\n')
    else:
      fout.write('\n')
    
    cursor.close()

  fout.write(r'    \end{tabu}' + '\n')
  fout.write(r'  \end{landscape}' + '\n')
  fout.write(r'\end{document}' + '\n')
  
  local_cnx.close()

def print_meeting(dayof, future=True):
  table = "future_meetings" if future else "known_meetings"
  
  local_cnx = mysql.connector.connect(                  \
            user='tm', password='dhmtks52',             \
            host='localhost', database='toastmasters')

  print "------------ MEETING ON {} -----------".format(str(dayof))
  for role in SQL_MEETING_ROLES:
    query = 'SELECT fname, lname, title, dayof, id, {} FROM '.format(role) \
            + '{} INNER JOIN members ON id = {} '.format(table, role) \
            + 'WHERE dayof = "{}"'.format(str(dayof))
    cursor = local_cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
      print "{}: {} {}, {}".format(role, rows[0][0], rows[0][1], rows[0][2])
    else:
      print "{}: ---".format(role)
    cursor.close()

  print "--------------------------------------"

  local_cnx.close()
