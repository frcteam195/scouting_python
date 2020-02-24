import mysql.connector as mariaDB
# For each analysisType we create add a new import statement. We could import all analysisTypes
from analysisTypes.autonomous import autonomous
from analysisTypes.ballSummary import ballSummary
from analysisTypes.brokeDown import brokeDown
from analysisTypes.climb import climb
from analysisTypes.groundPickup import groundPickup
from analysisTypes.hopperLoad import hopperLoad
from analysisTypes.lostComm import lostComm
from analysisTypes.matchVideos import matchVideos
from analysisTypes.playedDefense import playedDefense
from analysisTypes.startingPosition import startingPosition
from analysisTypes.subSBroke import subSBroke
from analysisTypes.totalBalls import totalBalls
from analysisTypes.totalInnerBalls import totalInnerBalls
from analysisTypes.totalLowBalls import totalLowBalls
from analysisTypes.totalOuterBalls import totalOuterBalls
from analysisTypes.totalScore import totalScore
from analysisTypes.totalUpperBalls import totalUpperBalls
from analysisTypes.wheelStage2 import wheelStage2
from analysisTypes.wheelStage3 import wheelStage3

from analysisTypes.startingPosition import startingPosition

# Define a Class called analysis
class analysis():
    # Inside the class there are several functions defined _run_query, _setColumns, _wipeCEA, _getTeams,
    #   _getTeamData, _analyzeTeams, and _insertAnalysis. Those functions will not get called automatically
    #   so in order to get them to run we create a __init__ function which is a special function in Python
    #   that gets run every time the Class is initialized. Here we build the DB connection cursor from within
    #   the __init__ function and then call the cursor, columns, wipeCEA, rsRobots, and analyzeTeams functions
    #   from within the __init__ function, which means they will be run automatically when the Class is initialized
    def __init__(self):
        # Connection to AWS Testing database - use when you would destroy tables with proper data
        # conn = mariaDB.connect(user='admin',
        #                        passwd='Einstein195',
        #                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
        #                        database='team195_scouting')

        # Connection to AWS database with proper data
        self.conn = mariaDB.connect(user='admin',
                               passwd='Einstein195',
                               host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                               database='team195_scouting')

        self.cursor = self.conn.cursor()
        self.columns = []
        self._wipeCEA()
        self.rsRobots = self._getTeams()
        self._analyzeTeams()

    # Function to run a query - the query string must be passed to the function
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEA table. We may want to make this only remove CurrentEvent records.
    def _wipeCEA(self):
        self._run_query("DELETE FROM CurrentEventAnalysis")
        self.conn.commit()

    # Function to get the team list and set it to rsRobots. Uses the _run_query function defined above.
    #   The assert statement will return rsRobots if the record length > 0 and will exit with the
    #       message "No robots founds" if the record length is 0.
    def _getTeams(self):
        self._run_query("SELECT MatchScouting.Team FROM (MatchScouting "
                       "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
                       "INNER JOIN Events ON Matches.EventID = Events.EventID "
                       "WHERE (((Events.CurrentEvent) = 1)) "
                       "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
                       "HAVING (((MatchScouting.Team) Is Not Null)); ")
        rsRobots = self.cursor.fetchall()

        assert len(rsRobots) > 0, "No robots found"
        return rsRobots

    # Function to retrieve data records for a given team for all their matches and set it to rsRobotMatches
    def _getTeamData(self, team):
        self._run_query("SELECT MatchScouting.*, Matches.MatchNo, Teams.RobotWeight "
            "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
            "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
            "AND (Matches.MatchID = MatchScouting.MatchID) "
            "INNER JOIN Teams ON (MatchScouting.Team = Teams.Team) "
            "WHERE (((MatchScouting.Team) = " + team[0] + " "
            "AND ((Events.CurrentEvent) = 1))"
            "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
            "AND (MatchScouting.TeamMatchNo <= 12)) "
            "ORDER BY MatchScouting.TeamMatchNo;")

        # Set columns to be a list of column headings in the Query results
        # Very cool - cursor.description is used to auto-determine the column headings in the MatchScouting table
        #   so these values do not need to be hard-coded
        self._setColumns([column[0] for column in list(self.cursor.description)])

        rsRobotMatches = self.cursor.fetchall()

        # If rsRobotMatches is not zero length return rsRobotMatches otherwise return None. This allows the
        #   function to skip a robot analysis if that robot does not have any match records yet.
        if rsRobotMatches:
            return rsRobotMatches
        else:
            return None

    #
    def _analyzeTeams(self):
        # Loop over the # of teams and run each of the analysis functions calling _insertAnalysis after each one is run
        for team in self.rsRobots:
            # print(team)
            rsRobotMatches = self._getTeamData(team)
            # print(rsRobotMatches)

            if rsRobotMatches:
                rsCEA = autonomous(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = ballSummary(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = brokeDown(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = climb(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = groundPickup(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = hopperLoad(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = lostComm(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = matchVideos(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = playedDefense(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = startingPosition(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = subSBroke(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalInnerBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalLowBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalOuterBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalScore(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = totalUpperBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = wheelStage2(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = wheelStage3(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)


    # Function to insert an rsCEA record into the DB.
    def _insertAnalysis(self, rsCEA):
        rsCEA_records = rsCEA.items()
        # Get the columnHeadings and values, do some formatting, and then use the _run_query function to run the
        #   query and the conn.commit to insert into the DB.
        columnHeadings = str(tuple([record[0] for record in rsCEA_records])).replace("'", "")
        values = str(tuple([record[1] for record in rsCEA_records]))

        # Insert the records into the DB
        self._run_query("INSERT INTO CurrentEventAnalysis "
                        + columnHeadings + " VALUES "
                        + values + ";")
        # print(columnHeadings + values)
        self.conn.commit()


# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()
