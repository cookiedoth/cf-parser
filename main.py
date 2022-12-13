import requests
import csv
from tqdm import tqdm
from problem_parser import parse_problem
from split import split

# Find the list of names of problems which are already saved
parsed_names = set()
try:
	csvfile = open('cf.csv', newline='')
	reader = csv.DictReader(csvfile)
	parsed_names = set(map(lambda dct : dct['name'], reader))
	parsed_names.remove('name')
	csvfile.close()
except FileNotFoundError:
	pass

# Find the list of urls which we were not able to parse (need to be skipped)
skip = set()
try:
	with open('bad_urls') as f:
		skip = set(map(lambda x: x.rstrip(), f.readlines()))
except FileNotFoundError:
	pass

f = open('cf.csv', 'a')
writer = csv.writer(f)
headers = ['name', 'legend', 'input', 'output', 'note', 'time_limit', 'memory_limit', 'rating', 'tags']
writer.writerow(headers)

problems = requests.get("https://codeforces.com/api/problemset.problems").json()

for problem in tqdm(problems['result']['problems']):
	if problem['name'] in parsed_names:
		continue
	contestId = problem['contestId']
	index = problem['index']
	url = f'https://codeforces.com/contest/{contestId}/problem/{index}'
	if url in skip:
		continue
	try:
		problem_data = parse_problem(url)
	except Exception as e:
		with open('err', 'a') as err:
			print(f'Cannot parse {url}', file=err)
		with open('bad_urls', 'a') as bad_urls:
			print(url, file=bad_urls)
		continue
	row = [
		problem['name'],
		problem_data.get('legend', ''),
		problem_data.get('input', ''),
		problem_data.get('output', ''),
		problem_data.get('note', ''),
		problem_data.get('time_limit', ''),
		problem_data.get('memory_limit', ''),
		problem.get('rating', ''),
		','.join(problem.get('tags', []))
	]
	writer.writerow(row)

f.close()

print('Splitting...')
split()

