import csv

students = list()
with open("my.csv", "r") as f:
    reader = csv.reader(f)
    for row in list(reader)[1:]:
        students.append(row)