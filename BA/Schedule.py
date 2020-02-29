import mysql.connector as mariaDB
import tbapy
import string
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195

def sortbymatch(d):
    return d.get('match_number', None)


conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()
cursor.execute("DELETE FROM BlueAllianceSchedule")
conn.commit()

team = tba.team(x)
cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = str(cursor.fetchone()[0])
print(event)

eventMatchListRed = []
eventMatchListBlue = []
matchNumberList = []
eventMatches = tba.event_matches(event)
for match in eventMatches:
    if match.comp_level == 'qm':
        matchNumberList.append(match.match_number)
matchNumberList = sorted(matchNumberList)
# print(matchNumberList)

for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['blue'] = match.alliances.get('blue').get('team_keys')
        matchNumber['blue'] = [key.replace('frc', '') for key in matchNumber['blue']]
        eventMatchListBlue.append(matchNumber)
# print(eventMatchListBlue)

for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['red'] = match.alliances.get('red').get('team_keys')
        matchNumber['red'] = [key.replace('frc', '') for key in matchNumber['red']]
        eventMatchListRed.append(matchNumber)
# print(eventMatchListRed)

for match in matchNumberList:
    Red1 = eventMatchListRed[match - 1].get('red')[0]
    Red2 = eventMatchListRed[match - 1].get('red')[1]
    Red3 = eventMatchListRed[match - 1].get('red')[2]
    Blue1 = eventMatchListBlue[match - 1].get('blue')[0]
    Blue2 = eventMatchListBlue[match - 1].get('blue')[1]
    Blue3 = eventMatchListBlue[match - 1].get('blue')[2]
    query = "INSERT INTO BlueAllianceSchedule (MatchNo, RedTeam1, RedTeam2, RedTeam3, BlueTeam1, BlueTeam2, " \
            "BlueTeam3) VALUES " + "('" + str(match) + "', '" + str(Red1) + "', '" + str(Red2) + "', '" + str(Red3) + \
            "', '" + str(Blue1) + "', '" + str(Blue2) + "', '" + str(Blue3) + "');"
    cursor.execute(query)
    conn.commit()
