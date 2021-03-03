import xlsxwriter
import datetime

workbook = xlsxwriter.Workbook('Challenges.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

expenses = (
    ['Gym',   datetime.datetime.date],
)


for item, cost in (expenses):
    worksheet.write(row, col, item)
    worksheet.write_datetime(row, col+1, cost)
    row += 1

workbook.close()
