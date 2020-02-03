import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Events;")

rsRobots = cursor.fetchall()
print(len(rsRobots))