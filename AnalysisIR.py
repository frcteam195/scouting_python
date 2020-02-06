import mysql.connector as mariaDB

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT MatchScouting.Team FROM (MatchScouting "
               "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
               "INNER JOIN Events ON Matches.EventID = Events.EventID "
               "WHERE (((Events.CurrentEvent) = 1)) "
               "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
               "HAVING (((MatchScouting.Team) Is Not Null)); ")
rsRobots = cursor.fetchall()
print(len(rsRobots))

if len(rsRobots) == 0:
    exit(1)

for row in rsRobots:
    cursor.execute("SELECT MatchScouting.*, Matches.MatchNo "
                   "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
                   "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
                   "AND (Matches.MatchID = MatchScouting.MatchID) "
                   "WHERE (((MatchScouting.Team) = " + row[0] + " "
                   "AND ((Events.CurrentEvent) = 1))"
                   "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
                   "AND (MatchScouting.TeamMatchNo <= 12)) "
                   "ORDER BY MatchScouting.TeamMatchNo;")

    columns = [column[0] for column in list(cursor.description)]

    rsRobotMatches = cursor.fetchall()
    print(len(rsRobotMatches))
    print(rsRobotMatches)

'''
columns = [column[0] for column in cursor.description]
print(columns)
results = []
for row in cursor.fetchall():
    results.append(dict(zip(columns, row)))
print(results)
'''