import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Computers;")

def insertComputer(id, name, typeID, stationID, trainingMode, robotImagePath, matchVideoPath, redOnLeft, matchIDToAnalyze, offline, defenseAdmin, admin, fieldOrientation):
    CompID = id
    CompName = name
    CompTID = typeID
    SID = stationID
    TM = trainingMode
    RIP = robotImagePath
    MVP = matchVideoPath
    ROL = redOnLeft
    MIDToAn = matchIDToAnalyze
    Off = offline
    DA = defenseAdmin
    A = admin
    FO = fieldOrientation
    sql = "INSERT INTO Computers (ComputerID, ComputerName, ComputerTypeID, AllianceStationID, TrainingMode, RobotImagePath, MatchVideoPath, RedOnLeft, MatchIDToAnalyze, Offline, DefenseAdmin, Admin, FieldOrientation) VALUES (%i, %s, %i, %i, %b, %s, %s, %b, %i, %b, %b, %b, %i)"
    iden = (CompID, CompName, CompTID, SID, TM, RIP, MVP, ROL, MIDToAn, Off, DA, A, FO)

    cursor.execute(sql, iden)

    conn.commit()