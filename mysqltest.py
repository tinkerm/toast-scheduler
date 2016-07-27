import mysql.connector

cnx = mysql.connector.connect(user='tm', password='dhmtks52', \
        host='localhost', database='toastmasters')

cnx.close()
