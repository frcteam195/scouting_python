import statistics
import numpy as np


def wheelStage3(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 6
    numberOfMatchesPlayed = 0
    wheelStage3Status = 0
    wheelStage3StatusList = []
    wheelStage3TimeList = []
    wheelStage3AttemptsList = []

    # Loop through each match the robot played in.
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
            wheelStage3Attempts = matchResults[analysis.columns.index('TeleWheelStage3Attempts')]
            if wheelStage3Attempts > 1:
                wheelStage3Status = matchResults[analysis.columns.index('TeleWheelStage3Status')]
                if wheelStage3Status > 1:
                    wheelStage3StatusString = "*"
                else:
                    wheelStage3StatusString = ""
                wheelStage3StatusList.append(wheelStage3Status)

                wheelStage3Time = matchResults[analysis.columns.index('TeleWheelStage3Time')]
                if wheelStage3Time is None:
                    wheelStage3Time = 999  # That should never happen - leaving the 999 in to show if there is an issue
                wheelStage3TimeList.append(wheelStage3Time)
                # Write out the record
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage3Time) + wheelStage3StatusString
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = wheelStage3Time
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = "-"

            if wheelStage3Status == 1:
                if wheelStage3Time <= 5:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
                elif 5 < wheelStage3Time < 11:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
                elif 10 < wheelStage3Time < 16:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
                elif wheelStage3Time >= 16:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            elif wheelStage3Attempts == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 0
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    # NOTE: All this needs to go above where the Display and Value records are created. It will not compile
    #       properly when the wheelStage3Status values can be evaluated without ensuring that it is acutally set
    #       This is fixed if this section is in the same level of the program and not one level higher.


    if len(wheelStage3StatusList) != 0:
        rsCEA['Summary1Display'] = statistics.mean(wheelStage3TimeList)
        rsCEA['Summary1Value'] = statistics.mean(wheelStage3TimeList)
        rsCEA['Summary2Display'] = statistics.median(wheelStage3TimeList)
        rsCEA['Summary2Value'] = statistics.median(wheelStage3TimeList)
        rsCEA['Summary3Display'] = np.sum(wheelStage3StatusList)/len(wheelStage3StatusList)*100
        rsCEA['Summary3Value'] = np.sum(wheelStage3StatusList)/len(wheelStage3StatusList)*100

        # Set the Display, Value, and Format values


    return rsCEA