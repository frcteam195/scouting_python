import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Events;")


def insertEvent(id, eventname, loc, start, end, current):
    EID = id
    EName = eventname
    ELoc = loc
    SD = start
    ED = end
    CE = current
    cursor.execute("INSERT INTO Events (EventID, EventName, EventLocation, StartDate, EndDate, CurrentEvent) "
               "VALUES (%i, %s, %s, %i, %i, %b)", (EID, EName, ELoc, SD, ED, CE))

insertEvent(4, 'Carson', 'Detroit', 20200304, 20200306, 0)

conn.commit()

for EventID in cursor:
    print(EventID)