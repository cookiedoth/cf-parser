import requests
import sys
from bs4 import BeautifulSoup

# returns a string
def parse_statement_part(tag):
	ps = tag.findChildren('p', recursive=False)
	return '\n'.join(map(lambda p : p.text, ps))

class_to_statement_part = {
	None: 'legend',
	'input-specification': 'input',
	'output-specification': 'output',
	'note': 'note'
}

err = open('err', 'w')
err.close()

# returns dictionary with keys "statement", "input", "output", "notes"
def parse_problem(url):
	err = open('err', 'a')
	result = {}
	html_doc = requests.get(url).text
	soup = BeautifulSoup(html_doc, 'html.parser')
	statement = soup.find('div', class_='problem-statement')
	for class_, name in class_to_statement_part.items():
		part = statement.findChildren('div', attrs={'class': class_}, recursive=False)
		if len(part) != 1:
			print(f'Skipped {url} {name}, {len(part)} tags found', file=err)
			continue
		parsed = parse_statement_part(part[0])
		if not parsed:
			print(f'Empty {url} {name}', file=err)
			continue
		result[name] = parsed
	return result

if __name__ == '__main__':
	url = 'https://codeforces.com/contest/1660/problem/A'
	parse_problem(url)
