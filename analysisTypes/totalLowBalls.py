import statistics
# ******************** AnalysisTypeID = 8 = Total Low Balls *******************

def totalBalls(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 3
    numberOfMatchesPlayed = 0
    totalHighBallsList = []
    totalBallsList = []

    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            TeleBallLowZone1 = matchResults[analysis.columns.index('TeleBallLowZone1')]
            if TeleBallLowZone1 is None:
                TeleBallLowZone1 = 0

            TeleBallOuterZone1 = matchResults[analysis.columns.index('TeleBallOuterZone1')]
            if TeleBallOuterZone1 is None:
                TeleBallOuterZone1 = 0

            TeleBallInnerZone1 = matchResults[analysis.columns.index('TeleBallInnerZone1')]
            if TeleBallInnerZone1 is None:
                TeleBallInnerZone1 = 0

            TeleBallOuterZone2 = matchResults[analysis.columns.index('TeleBallOuterZone2')]
            if TeleBallOuterZone2 is None:
                TeleBallOuterZone2 = 0

            TeleBallInnerZone2 = matchResults[analysis.columns.index('TeleBallInnerZone2')]
            if TeleBallInnerZone2 is None:
                TeleBallInnerZone2 = 0

            TeleBallOuterZone3 = matchResults[analysis.columns.index('TeleBallOuterZone3')]
            if TeleBallOuterZone3 is None:
                TeleBallOuterZone3 = 0

            TeleBallInnerZone3 = matchResults[analysis.columns.index('TeleBallInnerZone3')]
            if TeleBallInnerZone3 is None:
                TeleBallInnerZone3 = 0

            TeleBallOuterZone4 = matchResults[analysis.columns.index('TeleBallOuterZone4')]
            if TeleBallOuterZone4 is None:
                TeleBallOuterZone4 = 0

            TeleBallInnerZone4 = matchResults[analysis.columns.index('TeleBallInnerZone4')]
            if TeleBallInnerZone4 is None:
                TeleBallInnerZone4 = 0

            TeleBallOuterZone5 = matchResults[analysis.columns.index('TeleBallOuterZone5')]
            if TeleBallOuterZone5 is None:
                TeleBallOuterZone5 = 0

            TeleBallInnerZone5 = matchResults[analysis.columns.index('TeleBallInnerZone5')]
            if TeleBallInnerZone5 is None:
                TeleBallInnerZone5 = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalHighBalls = (TeleBallOuterZone1 + TeleBallInnerZone1 + TeleBallOuterZone2 +
                             TeleBallInnerZone2 + TeleBallOuterZone3 + TeleBallInnerZone3 +
                             TeleBallOuterZone4 + TeleBallInnerZone4 + TeleBallOuterZone5 +
                             TeleBallInnerZone5)
            totalBalls = totalHighBalls + TeleBallLowZone1
            totalHighBallsList.append(TeleBallOuterZone1 + TeleBallInnerZone1 + TeleBallOuterZone2 +
                                      TeleBallInnerZone2 + TeleBallOuterZone3 + TeleBallInnerZone3 +
                                      TeleBallOuterZone4 + TeleBallInnerZone4 + TeleBallOuterZone5 +
                                      TeleBallInnerZone5)
            totalBallsList.append(TeleBallOuterZone1 + TeleBallInnerZone1 + TeleBallOuterZone2 +
                                  TeleBallInnerZone2 + TeleBallOuterZone3 + TeleBallInnerZone3 +
                                  TeleBallOuterZone4 + TeleBallInnerZone4 + TeleBallOuterZone5 +
                                  TeleBallInnerZone5 + TeleBallLowZone1)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                str(TeleBallLowZone1) + "|" + str(totalBalls)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalBalls
            if totalBalls >= 30:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif 29 <= totalBalls >= 20:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif 19 <= totalBalls >= 10:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif 9 <= totalBalls >= 1:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else :
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalBallsList)
        rsCEA['Summary1Value'] = statistics.mean(totalBallsList)
        rsCEA['Summary2Display'] = statistics.median(totalBallsList)
        rsCEA['Summary2Value'] = statistics.median(totalBallsList)
        rsCEA['Summary3Display'] = statistics.mean(totalHighBallsList)
        rsCEA['Summary3Value'] = statistics.mean(totalHighBallsList)

    return rsCEA