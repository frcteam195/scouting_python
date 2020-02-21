import statistics
import numpy as np


def wheelStage2(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 5
    numberOfMatchesPlayed = 0
    wheelStage2StatusList = []
    wheelStage2TimeList = []
    wheelStage2AttemptsList = []

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
            wheelStage2Attempts = matchResults[analysis.columns.index('TeleWheelStage2Attempts')]
            if wheelStage2Attempts < 0:
                wheelStage2Status = matchResults[analysis.columns.index('TeleWheelStage2Status')]
                if wheelStage2Status > 1:
                    wheelStage2StatusString = "*"
                else:
                    wheelStage2StatusString = ""
                wheelStage2StatusList.append(wheelStage2Status)

                wheelStage2Time = matchResults[analysis.columns.index('TeleWheelStage2Time')]
                if wheelStage2Time is None:
                    wheelStage2Time = 999  # That should never happen - leaving the 999 in to show if there is an issue
                wheelStage2TimeList.append(wheelStage2Time)

                wheelStage2AttemptsList.append(wheelStage2Attempts)
                # Write the record
                numberOfMatchesPlayed += 1
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage2Time) + wheelStage2StatusString
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = wheelStage2Time
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = "-"

    if len(wheelStage2StatusList) != 0:
        rsCEA['Summary1Display'] = statistics.mean(wheelStage2TimeList)
        rsCEA['Summary1Value'] = statistics.mean(wheelStage2TimeList)
        rsCEA['Summary2Display'] = statistics.median(wheelStage2TimeList)
        rsCEA['Summary2Value'] = statistics.median(wheelStage2TimeList)
        rsCEA['Summary3Display'] = np.sum(wheelStage2StatusList) / len(wheelStage2StatusList) * 100
        rsCEA['Summary3Value'] = np.sum(wheelStage2StatusList) / len(wheelStage2StatusList) * 100
        # NEED TO ADD SOME COLORS

    return rsCEA
