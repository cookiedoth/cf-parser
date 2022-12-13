import csv

csvfile = open('cf.csv', newline='')
reader = csv.DictReader(csvfile)

len_sorted = []
name_to_problem = {}
tot_len = 0
tot_tags = 0
tot_problems = 0

for problem in reader:
	if problem['name'] == 'name':
		continue
	name_to_problem[problem['name']] = problem
	tot_len += len(problem['legend']) + len(problem['input']) + len(problem['output']) + len(problem['note'])
	tot_tags += len(problem['tags'].split(','))
	tot_problems += 1

print(f'Average length: {tot_len / tot_problems}')
print(f'Average tag count: {tot_tags / tot_problems}')
