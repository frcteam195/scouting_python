import mysql.connector as mariaDB

# Connection to AWS database with proper data
conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT Matches.* FROM Matches LEFT JOIN MatchScouting  "
                "ON (Matches.EventID = MatchScouting.EventID) "
                "AND Matches.MatchID = MatchScouting.MatchID "
                "WHERE (((Matches.EventID) = 1) AND ((MatchScouting.MatchID) is Null));")
columns = [column[0] for column in cursor.description]
print()
print(columns)
print()

#cursor.execute("SELECT * From Matches;")
rsMatches = []
# rsMatchScoutingRecords{}
for row in cursor.fetchall():
    i = 1
    while i <= 6:
        rsMatchScoutingRecord = {}
        rsMatchScoutingRecord['MatchID'] = row[0]
        rsMatchScoutingRecord['EventID'] = row[1]
        rsMatchScoutingRecord['Team'] = row[i+2]
        rsMatchScoutingRecord['AllianceStationID'] = i
        print(rsMatchScoutingRecord)
        items = rsMatchScoutingRecord.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))
        cursor.execute("INSERT INTO MatchScouting "
                       + columns + " VALUES "
                       + values + ";")
        conn.commit()
        i+=1

# items = rsCEA.items()
# columns = str(tuple([x[0] for x in items])).replace("'", "")
# values = str(tuple([x[1] for x in items]))
#
# cursor.execute("INSERT INTO [Current Event Analysis] "
#                + columns + " VALUES "
#                + values + ";")
# cursor.commit()

