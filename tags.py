import csv
import requests

print('Getting correct tags')
problems = requests.get("https://codeforces.com/api/problemset.problems").json()
problem_to_tags = {}

tags = set()
for problem in problems['result']['problems']:
	for tag in problem.get('tags', []):
		tags.add(tag)
print(len(tags))
