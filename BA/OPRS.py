import tbapy
import xlsxwriter
import operator
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

workbooko = xlsxwriter.Workbook('OPRS.xlsx')
worksheeto = workbooko.add_worksheet()

event = '2019necmp'
row = 0
col = 0

eventOpr = tba.event_oprs(event).get("oprs")

eventoprSorted = [(k[3:], eventOpr[k]) for k in sorted(eventOpr, key=eventOpr.get, reverse=True)]

for team in eventoprSorted:
    worksheeto.write_row(row, col , team)
    row += 1

workbooko.close()