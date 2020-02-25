import tbapy
import xlsxwriter
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

def sortbymatch(d):
    return d.get('match_number', None)


workbook = xlsxwriter.Workbook('SCHEDULE.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
worksheet.write(col, 0, 'MatchNo')
worksheet.write(col, 1, 'RedTeam1')
worksheet.write(col, 2, 'RedTeam2')
worksheet.write(col, 3, 'RedTeam3')
worksheet.write(col, 4, 'BlueTeam1')
worksheet.write(col, 5, 'BlueTeam2')
worksheet.write(col, 6, 'BlueTeam3')

event = '2019cur'

eventmatchList = []
eventMatches = tba.event_matches(event)

numberMatch = []
for match in eventMatches:
    if match.comp_level == 'qm':
        numberMatch.append(match.match_number)

row = 1
numberMatch.sort()
for matches in numberMatch:
    #numberMatch.sort()
    worksheet.write(row, col, matches)
    row += 1


row = 1
col = 4
for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['blue'] = match.alliances.get('blue').get('team_keys')
        matchNumber['blue'] = [key.replace('frc', '') for key in matchNumber['blue']]
    #if match.comp_level == 'qm':
        eventmatchList.append(matchNumber)
        for key in matchNumber.keys():
            worksheet.write_row(row, col, matchNumber[key])
        row += 1

row = 1
col = 1
for match in sorted(eventMatches, key=sortbymatch):
    if match.comp_level == 'qm':
        matchNumber = {}
        matchNumber['red'] = match.alliances.get('red').get('team_keys')
        matchNumber['red'] = [key.replace('frc', '') for key in matchNumber['red']]
        eventmatchList.append(matchNumber)
        for key in matchNumber.keys():
            worksheet.write_row(row, col, matchNumber[key])
        row += 1


workbook.close()










