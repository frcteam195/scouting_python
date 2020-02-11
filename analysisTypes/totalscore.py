import statistics
import numpy as np


# ******************** AnalysisTypeID = 4 = Starting Position *******************

def totalScore(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 4
    numberOfMatchesPlayed = 0
    ballsScoredLowMultiplier = 1
    ballsScoredOuterMultiplier = 2
    ballsScoredInnerMultiplier = 3
    autoMoveBonusMultiplier = 5
    rotationControlMultiplier = 10
    positionControlMultiplier = 20
    climbPointsMultiplier = 25
    parkPointsMultiplier = 5
    levelPointsMultiplier = 15
    totalPointsList = []

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        # to overwrite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        # Identify the various different types of scoring
        autoMoveBonus = matchResults[analysis.columns.index('AutoMoveBonus')]
        autoBallsLow = matchResults[analysis.columns.index('AutoBallLow')]
        autoBallsOuter = matchResults[analysis.columns.index('AutoBallOuter')]
        autoBallsInner = matchResults[analysis.columns.index('AutoBallInner')]
        teleBallsLow = matchResults[analysis.columns.index('TeleBallLowZone1')]
        teleBallsOuter = matchResults[analysis.columns.index('TeleBallOuterZone1')] + \
                         matchResults[analysis.columns.index('TeleBallOuterZone2')] + \
                         matchResults[analysis.columns.index('TeleBallOuterZone3')] + \
                         matchResults[analysis.columns.index('TeleBallOuterZone4')] + \
                         matchResults[analysis.columns.index('TeleBallOuterZone5')]
        teleBallsInner = matchResults[analysis.columns.index('TeleBallInnerZone1')] + \
                         matchResults[analysis.columns.index('TeleBallInnerZone2')] + \
                         matchResults[analysis.columns.index('TeleBallInnerZone3')] + \
                         matchResults[analysis.columns.index('TeleBallInnerZone4')] + \
                         matchResults[analysis.columns.index('TeleBallInnerZone5')]
        rotationControl = matchResults[analysis.columns.index('TeleWheelStage2Status')]
        positionControl = matchResults[analysis.columns.index('TeleWheelStage3Status')]
        if matchResults[analysis.columns.index('ClimbStatus')] == 1:
            if matchResults[analysis.columns.index('ClimbStatus')] > 0:
                climbPoints = 1
                parkPoints = 0
            else:
                climbPoints = 0
                parkPoints = 1
        else:
            climbPoints = 0
            parkPoints = 0
        levelPoints = matchResults[analysis.columns.index('ClimbLevelStatus')]

        # Adding up all the previously identified elements
        totalPoints = (autoMoveBonusMultiplier * autoMoveBonus) + \
                      (ballsScoredLowMultiplier * autoBallsLow * 2) + \
                      (ballsScoredOuterMultiplier * autoBallsOuter * 2) + \
                      (ballsScoredInnerMultiplier * autoBallsInner * 2) + \
                      (ballsScoredLowMultiplier * teleBallsLow) + \
                      (ballsScoredOuterMultiplier * teleBallsOuter) + \
                      (ballsScoredInnerMultiplier * teleBallsInner) + \
                      (rotationControlMultiplier * rotationControl) + \
                      (positionControlMultiplier + positionControl) + \
                      (climbPointsMultiplier * climbPoints) + \
                      (parkPointsMultiplier * parkPoints) + \
                      (levelPointsMultiplier * levelPoints)
        totalPointsList.append(totalPoints)
        # Set the color
        rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = totalPoints
        rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalPoints
        if totalPoints >= 101:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
        elif 70 < totalPoints < 101:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
        elif 40 < totalPoints < 71:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
        elif 10 < totalPoints < 41:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
        else:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1
    # Set the summary questions
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalPointsList)
        rsCEA['Summary1Value'] = statistics.mean(totalPointsList)
        rsCEA['Summary2Display'] = statistics.median(totalPointsList)
        rsCEA['Summary2Value'] = statistics.median(totalPointsList)

    return rsCEA
