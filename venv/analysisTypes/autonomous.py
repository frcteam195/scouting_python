import statistics
import numpy as np

# ******************** AnalysisTypeID = 2 = autonomous *******************

def autonomous(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 2
    numberOfMatchesPlayed = 0

    totalHighBalls = 0
    totalBalls = 0
    totalHighBallsList = []
    totalBallsList = []
    #sumTotalHighBalls = 0
    #sumTotalBalls = 0
    #medianList = []

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        #   to overwite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        # We are hijacking the starting position to write DNS or UR. This should go to Auto as it will not
        #   likely be displayed on team picker pages.
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            autoMoveBonus = matchResults[analysis.columns.index('AutoMoveBonus')]
            autoPenalty = matchResults[analysis.columns.index('AutoPenalty')]
            if autoPenalty == 1:
                autoPenaltyString = "*"
            else:
                autoPenaltyString = ""
            autoBallLow = matchResults[analysis.columns.index('AutoBallLow')]
            if autoBallLow is None:
                autoBallLow = 0
            autoBallOuter = matchResults[analysis.columns.index('AutoBallOuter')]
            if autoBallOuter is None:
                autoBallOuter = 0
            autoBallInner = matchResults[analysis.columns.index('AutoBallInner')]
            if autoBallInner is None:
                autoBallInner = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalHighBalls = autoBallOuter + autoBallInner
            totalBalls = totalHighBalls + autoBallLow
            totalHighBallsList.append(autoBallOuter + autoBallInner)
            totalBallsList.append(autoBallLow + autoBallOuter + autoBallInner)

            # Create the rsCEA records for Dsiplay, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(totalBalls) + "|" + str(totalHighBalls) + autoPenaltyString
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalBalls
            if totalBalls > 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif totalBalls == 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif 1 <= totalBalls < 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            else:
                if autoMoveBonus == 1:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
                else:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = statistics.mean(totalBallsList)
        rsCEA['Summary1Value'] = statistics.mean(totalBallsList)
        rsCEA['Summary2Display'] = statistics.mean(totalHighBallsList)
        rsCEA['Summary2Value'] = statistics.mean(totalHighBallsList)
        rsCEA['Summary3Display'] = statistics.median(totalBallsList)
        rsCEA['Summary3Value'] = statistics.median(totalBallsList)
        # Some test code for calculating min, max, quantiles
        print(min(totalBallsList))
        print(max(totalBallsList))
        testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        print(np.quantile(testList, 0.25))

    return rsCEA