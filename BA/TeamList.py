import mysql.connector as mariaDB
import tbapy
import string
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)
event = '2020mawne'  # This is the key for the event

def sortbyteam(d):
    return d.get('team_number', None)


conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()
eventTeams = tba.event_teams(event)
teamList = []

for team in sorted(eventTeams, key=sortbyteam):
    tempNick = ''
    teams = []
    teams.append(team.team_number)
    teams.append(team.nickname)
    cityState = str(team.city) + ' ' + str(team.state_prov) + ' ' + str(team.country)
    teams.append(cityState)
    teamList.append(teams)
    for char in team.nickname:
        if char.isalnum() or char == ' ':
            tempNick += char
    values = "(" + str(team.team_number) + "," + team.nickname + "," + cityState + ")"
    query = "INSERT INTO BlueAllianceTeams (Team, TeamName, TeamLocation) VALUES " + "('" + str(team.team_number) + \
             "','" + tempNick + "','" + str(cityState) + "');"
    print(query)
    cursor.execute(query)
    conn.commit()

print(teamList)
print(query)
