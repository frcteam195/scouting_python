import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Events;")

'''
Field,Type,Null,Key,Default,Extra
EventID,int(11),NO,PRI,NULL,auto_increment
EventName,varchar(100),YES,,NULL,
EventLocation,varchar(100),YES,,NULL,
StartDate,date,YES,,NULL,
EndDate,date,YES,,NULL,
CurrentEvent,tinyint(1),YES,,0,
'''

def insertEvent(id, name, location, startDate, endDate, currentEvent):
    EventID = id
    EventName = name
    EventLocation = location
    SD = startDate
    ED = endDate
    CE = currentEvent
    sql = "INSERT INTO ComputerTypes (EventID, EventName, EventLocation, StartDate, EndDate, CurrentEvent) VALUES (%i, %s, %s, %d, %d, %i)"
    iden = (EventID, EventName, EventLocation, SD, ED, CE)

    cursor.execute(sql, iden)

    conn.commit()

def readComputer(id, name, location, startDate, endDate, currentEvent):
    test = {'Event ID' : id, 'Event Name' : name, 'Event Location' : location, 'Start Date' : startDate, 'End Date' : endDate, 'Current Event' : currentEvent}
    import json
    x = json.dumps(test)
    print(x)