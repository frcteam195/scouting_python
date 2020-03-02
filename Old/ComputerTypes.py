import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.ComputerTypes;")

def insertComputerType(id, type):
    CompTypeID = id
    CompType = type
    sql = "INSERT INTO ComputerTypes (ComputerTypeID, ComputerType) VALUES (%i, %s)"
    iden = (CompTypeID, CompType)

    cursor.execute(sql, iden)

    conn.commit()

def readComputer(id, type):
    test = {'Computer Type ID' : id, 'Computer Type' : type}
    import json
    x = json.dumps(test)
    print(x)