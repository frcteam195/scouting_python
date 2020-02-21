# import statistics


def matchVideos(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 70
    numberOfMatchesPlayed = 0


    for matchResults in rsRobotMatches: