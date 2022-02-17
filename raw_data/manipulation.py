import csv

f = open('xword (1).csv')
csv_f = csv.reader(f)

with open('db.csv', mode='w') as db_file:
    db_writer = csv.writer(db_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for row in csv_f:
    db_writer.writerow(row)

