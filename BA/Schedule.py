import mysql.connector as mariaDB
import tbapy
import string

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)
event = '2019cur'  # This is the key for the event


def sortbyteam(d):
    return d.get('team_number', None)


def sortbymatch(d):
    return d.get('match_number', None)


conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

eventMatchListRed = []
eventMatchListBlue = []
matchNumberList = []
eventMatches = tba.event_matches(event)

for match in eventMatches:
    if match.comp_level == 'qm':
        matchNumberList.append(match.match_number)
matchNumberList = sorted(matchNumberList)
print(matchNumberList)

for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['blue'] = match.alliances.get('blue').get('team_keys')
        matchNumber['blue'] = [key.replace('frc', '') for key in matchNumber['blue']]
        eventMatchListBlue.append(matchNumber)
print(eventMatchListBlue)

for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['red'] = match.alliances.get('red').get('team_keys')
        matchNumber['red'] = [key.replace('frc', '') for key in matchNumber['red']]
        eventMatchListRed.append(matchNumber)
print(eventMatchListRed)

# for match in matchNumberList:
#     query = "INSERT INTO BlueAllianceSchedule (MatchNo, RedTeam1, RedTeam2, RedTeam3, BlueTeam1, BlueTeam2, " \
#             "BlueTeam3) VALUES " + "('" + str(match) + "', '" + str(eventMatchListRed[match])
# print(query)
