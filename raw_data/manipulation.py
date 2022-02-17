import csv

f = open('xword (1).csv')
csv_f = csv.reader(f)

for i, v in enumerate(csv_f):
    if i < 10:
        print(v)