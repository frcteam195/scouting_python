import tbapy
import xlsxwriter
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

def sortbyteam(d):
    return d.get('team_number', None)

workbook = xlsxwriter.Workbook('TEAM LIST.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

z = '2019cur'

bold = workbook.add_format({'bold': True})
merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow'})

worksheet.write(col, 0, 'Team')
worksheet.write(col, 1, 'TeamName')
worksheet.write(col, 2, 'TeamLocation')

row = 1
eventTeams = tba.event_teams(z)
teamList = []
for team in sorted(eventTeams, key=sortbyteam):
    tems = []
    tems.append(team.team_number)
    tems.append(team.nickname)
    cityState = str(team.city) + ', ' + str(team.state_prov) + ' ' + str(team.country)
    tems.append(cityState)
    teamList.append(tems)
    for teams in teamList:
        for team in tems:
            worksheet.write_row(row, col, tems)
    row += 1
#tems.sort()"""
row = 1
print(teamList)
workbook.close()

print(tba.team_events(195, 2019, keys=True))
print(eventTeams)


