import statistics
# ******************** AnalysisTypeID = 5 = Did They Play Defense *******************

def didTheyPlayDefense(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 3
    numberOfMatchesPlayed = 0
    totalPlaysOfDefenseList = []

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
            TeleDefense = matchResults[analysis.columns.index('TeleDefense')]
            if TeleDefense is None:
                TeleDefense = 0

            numberOfMatchesPlayed += 1
            totalDefensePlays = TeleDefense
            totalPlaysOfDefenseList.append(totalDefensePlays)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                str(TeleDefense)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = TeleDefense

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalPlaysOfDefenseList)
        rsCEA['Summary1Value'] = statistics.mean(totalPlaysOfDefenseList)
        rsCEA['Summary2Display'] = statistics.median(totalPlaysOfDefenseList)
        rsCEA['Summary2Value'] = statistics.median(totalPlaysOfDefenseList)
        rsCEA['Summary3Display'] = statistics.mean(totalPlaysOfDefenseList)
        rsCEA['Summary3Value'] = statistics.mean(totalPlaysOfDefenseList)

    return rsCEA