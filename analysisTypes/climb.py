import statistics
# ******************** AnalysisTypeID = 7 = Climb *******************

def climb(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 7
    numberOfMatchesPlayed = 0
    totalClimbPointsList = []

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
            ClimbMoveOnBar = matchResults[analysis.columns.index('ClimbMoveOnBar')]
            if ClimbMoveOnBar == 1:
                ClimbMoveOnBarString = "*"
            else:
                ClimbMoveOnBarString = ""
            ClimbStatus = matchResults[analysis.columns.index('ClimbStatus')]
            if ClimbStatus is None:
                ClimbStatus = 0
            ClimbHeight = matchResults[analysis.columns.index('ClimbHeight')]
            if ClimbHeight is None:
                ClimbHeight = 0
            ClimbPosition = matchResults[analysis.columns.index('ClimbPosition')]
            if ClimbPosition is None:
                ClimbPosition = 0
            ClimbLevelStatus = matchResults[analysis.columns.index('ClimbLevelStatus')]
            if ClimbLevelStatus is None:
                ClimbLevelStatus = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalClimbPoints = ClimbStatus + ClimbHeight + ClimbPosition + ClimbLevelStatus
            totalClimbPointsList.append(ClimbStatus + ClimbHeight + ClimbPosition + ClimbLevelStatus)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                str(totalClimbPoints) + str(ClimbMoveOnBarString)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalClimbPoints
            if totalClimbPoints >= 40:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif 39 <= totalClimbPoints >= 30:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif 29 <= totalClimbPoints >= 20:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif 19 <= totalClimbPoints >= 5:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalClimbPointsList)
        rsCEA['Summary1Value'] = statistics.mean(totalClimbPointsList)
        rsCEA['Summary2Display'] = statistics.median(totalClimbPointsList)
        rsCEA['Summary2Value'] = statistics.median(totalClimbPointsList)
        rsCEA['Summary3Display'] = statistics.mean(totalClimbPointsList)
        rsCEA['Summary3Value'] = statistics.mean(totalClimbPointsList)

    return rsCEA