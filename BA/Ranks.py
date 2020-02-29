import mysql.connector as mariaDB
import tbapy
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

def sortbyteam(d):
    return d.get('team_number', None)


conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()


cursor.execute("DELETE FROM BlueAllianceRankings")
conn.commit()

cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]

eventTeams = tba.event_teams(event)
teamRanks = tba.event_rankings(event).get('rankings')
teamRankList = []
for teamRank in teamRanks:
    teamRankList.append(teamRank['team_key'][3:])

for team in teamRankList:
    query = "INSERT INTO BlueAllianceRankings (Team, TeamRank) VALUES " + "('" + str(team) + "', '" + \
            str(teamRankList.index(team) + 1) + "');"
    print(query)
    cursor.execute(query)
    conn.commit()