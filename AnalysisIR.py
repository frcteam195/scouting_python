import mysql.connector as mariaDB

# Connecting to CyberScouter DB
conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

# Delete CurrentEventAnalysis Table contents before beginning
#   Note, this may need to be modified to delete only records from the current event, or we modify things so that
#       at the time of Event creation a CEA_Event# table is built in the database so each event has its own table
cursor.execute("DELETE FROM CurrentEventAnalysis")
conn.commit()

# SQL Query to get list of teams for the current event and set it to rsRobots
cursor.execute("SELECT MatchScouting.Team FROM (MatchScouting "
               "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
               "INNER JOIN Events ON Matches.EventID = Events.EventID "
               "WHERE (((Events.CurrentEvent) = 1)) "
               "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
               "HAVING (((MatchScouting.Team) Is Not Null)); ")
rsRobots = cursor.fetchall()
#print(len(rsRobots))

# Exit if there are no robots in the current event - Sanity Check!
if len(rsRobots) == 0:
    exit(1)

# Loop over the # of teams in rsRobots and run a Query to create a rsRobotMatches record set with MatchScouting Results
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

    # Set columns to be a list of column headings in the Query results
    # Very cool - cursor.description is used to auto-determine the column headings in the MatchScouting table
    columns = [column[0] for column in list(cursor.description)]
    # Dump the results from the Query into the rsRobotMatches record set
    rsRobotMatches = cursor.fetchall()
    #print(len(rsRobotMatches))
    #print(rsRobotMatches)

    # Don't bother continuing if the robot has not played any matches
    if len(rsRobotMatches) > 0:
        NumberOfMatchesPlayed = 0
        # Initialize the rsCEA record set. Must be outside the for loop as it will wipe the record set when executed
        rsCEA = {}
        # Loop through each match the robot played in.
        for matchResults in rsRobotMatches:
            rsCEA ['Team'] = matchResults[columns.index('Team')]
            rsCEA['EventID'] = matchResults[columns.index('EventID')]
            rsCEA['AnalysisTypeID'] = 1

            # We are hijacking the starting position to write DNS or UR. This should go to auto as it will not
            #   likely be displayed on team picker pages.
            autoDidNotShow = matchResults[columns.index('AutoDidNotShow')]
            scoutingStatus = matchResults[columns.index('ScoutingStatus')]
            if autoDidNotShow == 1:
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
            elif scoutingStatus == 2:
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
            else:
                # Increment the number of matches played and write Match#Display, Match#Value and Match#Format
                NumberOfMatchesPlayed += 1
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Display'] = matchResults[columns.index('AutoStartPos')]
                rsCEA['Match' + str(matchResults[columns.index('TeamMatchNo')]) + 'Value'] = matchResults[columns.index('AutoStartPos')]
                # An if statement will go here to define Match#Format


        rsCEA_records = rsCEA.items()
        # print rsCEA_records dictionary for debugging
        #print(rsCEA_records)
        # Get columnHeadings and values from the rsCEA_records dictionary and do some formatting to get ready for DB insert
        columnHeadings = str(tuple([record[0] for record in rsCEA_records])).replace("'", "")
        values = str(tuple([record[1] for record in rsCEA_records]))
        #print(columnHeadings)
        #print(values)

        # Insert the records into the DB
        cursor.execute("INSERT INTO CurrentEventAnalysis "
                       + columnHeadings + " VALUES "
                       + values + ";")
        conn.commit()

#print(columns)