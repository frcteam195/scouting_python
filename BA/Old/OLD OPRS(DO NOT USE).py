import tbapy
import xlsxwriter
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

workbook = xlsxwriter.Workbook('OPRS.xlsx')
worksheet = workbook.add_worksheet()

event = '2019necmp'
row = 0
col = 0

eventOpr = tba.event_oprs(event).get("oprs")

eventoprSorted = [(k[3:], eventOpr[k]) for k in sorted(eventOpr, key=eventOpr.get, reverse=True)]

for team in eventoprSorted:
    worksheet.write_row(row, col , team)
    row += 1

workbook.close()