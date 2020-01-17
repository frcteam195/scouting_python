import pypyodbc
import statistics

connection = pypyodbc.connect(driver='{SQL Server}',
                              server='MACIEJEWSKI3\SQLEXPRESS',
                              database='CyberScouter',
                              uid='scout',
                              pwd='2qrobot!')

cursor = connection.cursor()

cursor.execute("DELETE FROM [Current Event Analysis]")
cursor.commit()

dataFlag = 0

"""cursor.execute("SELECT [Match Scouting].Team FROM ([Match Scouting] "
               "INNER JOIN Matches ON [Match Scouting].MatchID = Matches.MatchID) "
               "INNER JOIN Events ON Matches.EventID = Events.EventID "
               "WHERE (((Events.CurrentEvent) = -1)) "
               "GROUP BY CAST([Match Scouting].Team AS INT), [Match Scouting].Team "
               "HAVING ((([Match Scouting].Team) Is Not Null)); ")"""

cursor.execute("SELECT [Match Scouting].Team FROM ([Match Scouting] "
               "INNER JOIN Matches ON [Match Scouting].MatchID = Matches.MatchID) "
               "INNER JOIN Events ON Matches.EventID = Events.EventID "
               "WHERE (((Events.EventID) = 22)) "
               "GROUP BY CAST([Match Scouting].Team AS INT), [Match Scouting].Team "
               "HAVING ((([Match Scouting].Team) Is Not Null)); ")

rsRobots = cursor.fetchall()
print(len(rsRobots))

if len(rsRobots) == 0:
    exit(1)

for row in rsRobots:
    cursor.execute("SELECT [Match Scouting].*, [Matches].MatchNo "
                   "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
                   "INNER JOIN [Match Scouting] ON (Matches.EventID = [Match Scouting].EventID) "
                   "AND (Matches.MatchID = [Match Scouting].MatchID) "
                   "WHERE ((([Match Scouting].Team) = " + row[0] + " "
                   "AND ((Events.CurrentEvent) = 0))"
                   "AND (([ScoutingStatus] = 1) Or ([ScoutingStatus] = 2) Or ([ScoutingStatus] = 3)) "
                   "AND ([Match Scouting].TeamMatchNo <= 12)) "
                   "ORDER BY [Match Scouting].TeamMatchNo;")

    columns = [x[0] for x in list(cursor.description)]

    rsRobotMatches = cursor.fetchall()
    print(len(rsRobotMatches))

    if len(rsRobotMatches) > 0:
        dataFlag = 1

        '''
        ****************************
        ****** Autonomous **********
        ****************************
        '''

        SumAutoHatch = 0
        SumAutoCargo = 0
        TotalAutoHatch = 0
        TotalAutoCargo = 0
        TotalAuto = 0
        rs = 0
        NumberOfMatchesPlayed = 0
        MinValue = 0
        MaxValue = 0
        MedianArray = [0] * 100

        for r in rsRobotMatches:
            rsCEA = {}
            rsCEA['Team'] = r[columns.index('team')]
            rsCEA['EventID'] = r[columns.index('eventid')]
            rsCEA['AnalysisTypeID'] = 1

            auto_show = r[columns.index('autodidnotshow')]
            scouting_status = r[columns.index('scoutingstatus')]
            if auto_show == 1:
                rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Display'] = 'DNS'
            elif scouting_status == 2:
                rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Display'] = 'UR'
            else:
                NumberOfMatchesPlayed += 1

                auto_hatch_far_low = r[columns.index('autorshatchfarlow')]
                if auto_hatch_far_low is None:
                    auto_hatch_far_low = 0

                auto_hatch_far_med = r[columns.index('autorshatchfarmed')]
                if auto_hatch_far_med is None:
                    auto_hatch_far_med = 0

                auto_hatch_far_high = r[columns.index('autorshatchfarhigh')]
                if auto_hatch_far_high is None:
                    auto_hatch_far_high = 0

                auto_hatch_near_low = r[columns.index('autorshatchnearlow')]
                if auto_hatch_near_low is None:
                    auto_hatch_near_low = 0

                auto_hatch_near_med = r[columns.index('autorshatchnearmed')]
                if auto_hatch_near_med is None:
                    auto_hatch_near_med = 0

                auto_hatch_near_high = r[columns.index('autorshatchnearhigh')]
                if auto_hatch_near_high is None:
                    auto_hatch_near_high = 0

                rs = auto_hatch_near_low + auto_hatch_near_med + auto_hatch_near_high + auto_hatch_far_low + auto_hatch_far_med + auto_hatch_far_high

                auto_cs_hatch = r[columns.index('autocshatch')]
                if auto_cs_hatch is None:
                    auto_cs_hatch = 0

                auto_cs_cargo = r[columns.index('autocscargo')]
                if auto_cs_cargo is None:
                    auto_cs_cargo = 0

                auto_rs_cargo_low = r[columns.index('autorscargolow')]
                if auto_rs_cargo_low is None:
                    auto_rs_cargo_low = 0

                auto_rs_cargo_med = r[columns.index('autorscargomed')]
                if auto_rs_cargo_med is None:
                    auto_rs_cargo_med = 0

                auto_rs_cargo_high = r[columns.index('autorscargohigh')]
                if auto_rs_cargo_high is None:
                    auto_rs_cargo_high = 0

                totalAutoHatch = auto_cs_hatch + rs
                totalAutoCargo = auto_cs_cargo + auto_rs_cargo_low + auto_rs_cargo_med + auto_rs_cargo_high

                totalAuto = totalAutoHatch + totalAutoCargo

                if rs > 0:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Display'] = str(totalAuto) + '|' + \
                                                                                   str(totalAutoCargo) + '*'
                else:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Display'] = str(totalAuto) + '|' \
                                                                                        + str(totalAutoCargo)

                if totalAuto >= 3:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Format'] = 5
                elif totalAuto >= 2:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Format'] = 4
                elif totalAuto >= 1:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Format'] = 3
                else:
                    rsCEA['Match' + str(r[columns.index('teammatchno')]) + 'Format'] = 2

                SumAutoCargo += totalAutoCargo
                SumAutoHatch += TotalAutoHatch

                MedianArray[NumberOfMatchesPlayed-1] = TotalAuto

                if NumberOfMatchesPlayed == 1:
                    MinValue = TotalAuto
                    MaxValue = TotalAuto
                else:
                    MinValue = min(MinValue, totalAuto)
                    MaxValue = max(MaxValue, totalAuto)

        if NumberOfMatchesPlayed > 0:
            rsCEA['Summary1Display'] = str(round((SumAutoHatch + SumAutoCargo)/NumberOfMatchesPlayed, 1))
            rsCEA['Summary1Value'] = (SumAutoHatch + SumAutoCargo)/NumberOfMatchesPlayed

            rsCEA['Min'] = MinValue
            rsCEA['Max'] = MaxValue

            rsCEA['Summary2Display'] = statistics.median(MedianArray)
            rsCEA['Summary2Value'] = statistics.median(MedianArray)

        items = rsCEA.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))

        cursor.execute("INSERT INTO [Current Event Analysis] "
                       + columns + " VALUES "
                       + values + ";")
        cursor.commit()






