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
    sql = "INSERT INTO Events (EventID, EventName, EventLocation, StartDate, EndDate, CurrentEvent) VALUES (%i, %s, %s, %i, %i, %b)"
    '''val = (4, 'Carson', 'Detroit', 20200304, 20200306, 1)'''
    iden = (EID, EName, ELoc, SD, ED, CE)
    cursor.execute(sql, iden)
    '''insert val when you want to test assuming dan and betul get the print to work'''

    conn.commit()

    for EventID in cursor:
        print(EventID)







    '''
    cursor.execute("INSERT INTO Events (EventID, EventName, EventLocation, StartDate, EndDate, CurrentEvent) "
                   "VALUES (%i, %s, %s, %i, %i, %b)", (EID, EName, ELoc, SD, ED, CE))
                   
                   
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

insertEvent(4, 'Carson', 'Detroit', 20200304, 20200306, 1)
'''