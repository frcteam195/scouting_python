import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Computers;")

def insertComputer(id, name, typeID, connectionStatus, stationID):
    CompID = id
    CompName = name
    CompTID = typeID
    CS = connectionStatus
    SID = stationID
    sql = "INSERT INTO Computers (ComputerID, ComputerName, ComputerTypeID, ConnectionStatus, StationID) VALUES (%i, %s, %i, %b, %i)"
    iden = (CompID, CompName, CompTID, CS, SID)

    cursor.execute(sql, iden)

    conn.commit()

def readComputer(id, name, typeID, connectionStatus, stationID):
    test = {'Computer ID' : id, 'Computer Name' : name, 'Computer Type ID' : typeID, 'Connection Status' : connectionStatus, 'Station ID' : stationID}
    import json
    x = json.dumps(test)
    print(x)

readComputer(1, "Junk", 0, 0, 2)

# test