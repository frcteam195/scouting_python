import mysql.connector as mariaDB
import tbapy
import string
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
year = 2020

def sortbyteam(d):
    return d.get('team_number', None)

def onlyascii(s):
    return "".join(i for i in s if ord(i)<128 and ord(i)!=39)

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()
totalTeams = tba.teams(year=2020)
teamList = []

for team in totalTeams:
    tempNick = ''
    teamNum = team.get('team_number')
    cityState = str(team.city) + ' ' + str(team.state_prov) + ' ' + str(team.country)
    queryLocation = ''
    tempNick = onlyascii(team.nickname)
    if len(tempNick) > 50:
        tempNick = tempNick[:40]
    queryLocation = onlyascii(cityState)
    if len(queryLocation) > 50:
        queryLocation = queryLocation[:40]
    query = "INSERT INTO Teams (Team, TeamName, TeamLocation) VALUES " + "('" + str(team.team_number) + \
            "','" + str(tempNick) + "','" + str(queryLocation) + "');"
    print(query)
    cursor.execute(query)
    conn.commit()
