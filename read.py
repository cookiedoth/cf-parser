import csv
import requests

print('Getting correct tags')
problems = requests.get("https://codeforces.com/api/problemset.problems").json()
problem_to_tags = {}
for problem in problems['result']['problems']:
	problem_to_tags[problem['name']] = ','.join(problem.get('tags', []))

headers = ['name', 'legend', 'input', 'output', 'note', 'rating', 'tags']
rows = [headers]

print('Reading broken csv')
csvfile = open('cf.csv', newline='')
reader = csv.DictReader(csvfile)
for problem in reader:
	if problem['name'] == 'name':
		continue
	problem['tags'] = problem_to_tags[problem['name']]
	rows.append([problem[key] for key in headers])

csvfile.close()

print('Writing new csv')
f = open('cf_new.csv', 'w')
writer = csv.writer(f)
for row in rows:
	writer.writerow(row)
f.close()
