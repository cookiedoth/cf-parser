import csv
import random

random.seed(42)

csvfile = open('cf_new.csv', newline='')
reader = csv.DictReader(csvfile)

problems = list(reader)
random.shuffle(problems)

train_size = int(len(problems) * 0.8)

def save(lst, path):
	headers = ['name', 'legend', 'input', 'output', 'note', 'rating', 'tags']
	rows = [headers]
	f = open(path, 'w')
	for problem in lst:
		rows.append([problem[key] for key in headers])
	writer = csv.writer(f)
	for row in rows:
		writer.writerow(row)
	f.close()

save(problems[:train_size], 'cf_train.csv')
save(problems[train_size:], 'cf_test.csv')
