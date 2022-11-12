import csv

try:
	csvfile = open('cf.csv', newline='')
	reader = csv.DictReader(csvfile)
	for x in reader:
		print(x['rating'])
except FileNotFoundError:
	pass
