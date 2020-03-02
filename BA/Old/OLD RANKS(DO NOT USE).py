import tbapy
import xlsxwriter
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

workbook = xlsxwriter.Workbook('EVENT RANKINGS.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

event = '2019necmp'
bold = workbook.add_format({'bold': True})
merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow'})

matchesPlayed = tba.event_rankings(event).get('rankings')
matchesplayedDict = {}
for team in matchesPlayed:
    matchesplayedDict[team.get("rank")] = team.get("matches_played")

row = 1
col = 2
for key in matchesplayedDict.keys():
    worksheet.write(row, col, matchesplayedDict[key])
    row += 1


teamRanks = tba.event_rankings(event).get('rankings')
teamrankDict = {}
for rank in teamRanks:
    teamrankDict[rank.get("rank")] = rank.get("team_key")[3:]

row = 1
col = 0
for key in teamrankDict.keys():
    worksheet.write(row, col, key)
    worksheet.write(row, col + 1, teamrankDict[key])
    row += 1

print(teamRanks)

quals = tba.event_rankings(event).get('rankings')
qualAverage = {}
for team in quals:
    qualAverage[team.get("rank")] = team.get("qual_average")

row = 1
col = 3
for key in qualAverage.keys():
    worksheet.write(row, col, qualAverage[key])
    row += 1


print(teamRanks)
print(matchesplayedDict)
print(teamrankDict)
print(qualAverage)
workbook.close()