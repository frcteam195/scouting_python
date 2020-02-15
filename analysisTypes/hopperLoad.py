import statistics
import numpy as np


# ******************** AnalysisTypeID = 24 = Hopper Load *******************

def hopperLoad(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 24
    numberOfMatchesPlayed = 0
    wheelStage3StatusList = []
    wheelStage3TimeList = []
    wheelStage3AttemptsList = []

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
            