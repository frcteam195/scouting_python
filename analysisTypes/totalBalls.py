import statistics
import numpy as np
# ******************** AnalysisTypeID = 3 = Total Balls *******************

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

        ballLow = matchResults[analysis.columns.index('BallLow')]
        if ballLow is None:
            ballLow = 0
        ballOuter = matchResults[analysis.columns.index('AutoBallOuter')]
        if ballOuter is None:
            ballOuter = 0
        ballInner = matchResults[analysis.columns.index('AutoBallInner')]
        if ballInner is None:
            ballInner = 0

        numberOfMatchesPlayed += 1
        totalHighBalls = ballOuter + ballInner
        totalBalls = totalHighBalls + ballLow
        totalHighBallsList.append(ballOuter + ballInner)
        totalBallsList.append(ballLow + ballOuter + ballInner)

        rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(
            totalBalls) + "|" + str(totalHighBalls)
        rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalBalls
        if totalBalls > 3:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
        elif totalBalls == 3:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
        elif 1 <= totalBalls < 3:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalBallsList)
        rsCEA['Summary1Value'] = statistics.mean(totalBallsList)
        rsCEA['Summary2Display'] = statistics.mean(totalHighBallsList)
        rsCEA['Summary2Value'] = statistics.mean(totalHighBallsList)
        rsCEA['Summary3Display'] = statistics.median(totalBallsList)
        rsCEA['Summary3Value'] = statistics.median(totalBallsList)

    return rsCEA