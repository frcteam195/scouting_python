import mysql.connector as mariaDB

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("DELETE FROM CurrentEventAnalysis")
conn.commit()

cursor.execute("SELECT MatchScouting.Team FROM (MatchScouting "
               "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
               "INNER JOIN Events ON Matches.EventID = Events.EventID "
               "WHERE (((Events.CurrentEvent) = 1)) "
               "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
               "HAVING (((MatchScouting.Team) Is Not Null)); ")
rsRobots = cursor.fetchall()
#print(len(rsRobots))

if len(rsRobots) == 0:
    exit(1)

for team in rsRobots:
    cursor.execute("SELECT MatchScouting.*, Matches.MatchNo "
                   "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
                   "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
                   "AND (Matches.MatchID = MatchScouting.MatchID) "
                   "WHERE (((MatchScouting.Team) = " + team[0] + " "
                   "AND ((Events.CurrentEvent) = 1))"
                   "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
                   "AND (MatchScouting.TeamMatchNo <= 12)) "
                   "ORDER BY MatchScouting.TeamMatchNo;")

    columns = [column[0] for column in list(cursor.description)]
    rsRobotMatches = cursor.fetchall()
    #print(len(rsRobotMatches))
    #print(rsRobotMatches)

    if len(rsRobotMatches) > 0:
        NumberOfMatchesPlayed = 0
        rsCEA = {}
        for matchResults in rsRobotMatches:
            rsCEA ['Team'] = matchResults[columns.index('Team')]
            rsCEA['EventID'] = matchResults[columns.index('EventID')]
            rsCEA['AnalysisTypeID'] = 1

            autoDidNotShow = matchResults[columns.index('AutoDidNotShow')]
            scoutingStatus = matchResults[columns.index('ScoutingStatus')]
            if autoDidNotShow == 1:
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
            elif scoutingStatus == 2:
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
            else:
                NumberOfMatchesPlayed += 1
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = matchResults[columns.index('AutoStartPos')]
        print(team)
        items = rsCEA.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))

        cursor.execute("INSERT INTO CurrentEventAnalysis "
                       + columns + " VALUES "
                       + values + ";")
        conn.commit()

#print(columns)