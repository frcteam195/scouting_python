import statistics
# ******************** AnalysisTypeID = 5 = Wheel - Stage 2 *******************

def wheelStage2(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 3
    numberOfMatchesPlayed = 0
    teleWheelStage2StatusList = []
    teleWheelStage2TimeList = []
    teleWheelStage2AttemptsList = []

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
            TeleWheelStage2Status = matchResults[analysis.columns.index('TeleWheelStage2Status')]
            TeleWheelStage2Time = matchResults[analysis.columns.index('TeleWheelStage2Time')]
            TeleWheelStage2Attempts = matchResults[analysis.columns.index('TeleWheelStage2Attempts')]
            if TeleWheelStage2Status == 1:
                TeleWheelStage2Status = "*"
            if TeleWheelStage2Time is None:
                TeleWheelStage2Time = 0
            if TeleWheelStage2Attempts < 1:
                TeleWheelStage2Attempts = "-"

            numberOfMatchesPlayed += 1
            teleWheelStatus = TeleWheelStage2Status
            totalWheelTime = TeleWheelStage2Time
            totalWheelAttempts = TeleWheelStage2Attempts
            teleWheelStage2StatusList.append(teleWheelStatus)
            teleWheelStage2TimeList.append(totalWheelTime)
            teleWheelStage2AttemptsList.append(totalWheelAttempts)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                str(TeleWheelStage2Time) + TeleWheelStage2Attempts
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = TeleWheelStage2Time

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(teleWheelStage2TimeList)
        rsCEA['Summary1Value'] = statistics.mean(teleWheelStage2TimeList)
        rsCEA['Summary2Display'] = statistics.median(teleWheelStage2TimeList)
        rsCEA['Summary2Value'] = statistics.median(teleWheelStage2TimeList)
        rsCEA['Summary3Display'] = statistics.mean(teleWheelStage2TimeList)
        rsCEA['Summary3Value'] = statistics.mean(teleWheelStage2TimeList)

    return rsCEA