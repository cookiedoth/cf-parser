import csv
import random

def save(lst, path):
	headers = ['name', 'legend', 'input', 'output', 'note', 'time_limit',
		'memory_limit', 'rating', 'tags']
	rows = [headers]
	f = open(path, 'w')
	for problem in lst:
		rows.append([problem[key] for key in headers])
	writer = csv.writer(f)
	for row in rows:
		writer.writerow(row)
	f.close()

def split():
	random.seed(42)
	csvfile = open('cf.csv', newline='')
	reader = csv.DictReader(csvfile)

	problems = list(reader)
	random.shuffle(problems)

	train_size = int(len(problems) * 0.7)
	validate_size = int(len(problems) * 0.15)

	save(problems[:train_size], 'cf_train.csv')
	save(problems[train_size : train_size + validate_size], 'cf_validate.csv')
	save(problems[train_size + validate_size:], 'cf_test.csv')
