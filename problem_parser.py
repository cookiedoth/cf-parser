import requests
import sys
from bs4 import BeautifulSoup
import pprint
import re


def parse_statement_part(tag):
	ch = list(filter(lambda tag: tag.name == 'li' or tag.name == 'p', tag.find_all()))
	return '\n'.join(map(lambda p : p.text, ch))


def parse_constraint(tag):
	occ = re.findall('\\d+', tag.text)
	return occ[0] if len(occ) == 1 else None


statement_part_class = {
	'legend': None,
	'input': 'input-specification',
	'output': 'output-specification',
	'note': 'note'
}

constraint_class = {
	'time_limit': 'time-limit',
	'memory_limit': 'memory-limit'
}

err = open('err', 'w')
err.close()


def fetch_problem_parameter(url, statement, name, class_name, recursive, tag_count, tag_id, downstream_parser, result, err):
	tags = statement.findChildren('div', attrs={'class': class_name}, recursive=recursive)
	parsed = downstream_parser(tags[tag_id]) if len(tags) == tag_count else None
	if parsed is None or parsed == '':
		print(f'Did not parse {url} {name}', file=err)
	else:
		result[name] = parsed


def is_interactive(statement):
	return any('Interaction' in tag.text for tag in
		statement.findChildren('div', attrs={'class': 'section-title'}))


def parse_statement_interactive(url, statement, result, err):
	fetch_problem_parameter(
		url, statement, 'legend', None,
		False, 2, 0, parse_statement_part, result, err)
	fetch_problem_parameter(
		url, statement, 'input', None,
		False, 2, 1, parse_statement_part, result, err)
	fetch_problem_parameter(
		url, statement, 'note', 'note',
		False, 1, 0, parse_statement_part, result, err)


def parse_statement_non_interactive(url, statement, result, err):
	for name, class_name in statement_part_class.items():
		fetch_problem_parameter(
			url, statement, name, class_name,
			False, 1, 0, parse_statement_part, result, err)


def parse_all_constrains(url, statement, result, err):
	for name, class_name in constraint_class.items():
		fetch_problem_parameter(
			url, statement, name, class_name,
			True, 1, 0, parse_constraint, result, err)


# returns dictionary with keys "statement", "input", "output",
# "notes", "time_limit", "memory_limit"
def parse_problem(url):
	err = open('err', 'a')
	result = {}
	html_doc = requests.get(url).text
	soup = BeautifulSoup(html_doc, 'html.parser')
	statement = soup.find('div', class_='problem-statement')

	if is_interactive(statement):
		parse_statement_interactive(url, statement, result, err)
	else:
		parse_statement_non_interactive(url, statement, result, err)

	parse_all_constrains(url, statement, result, err)

	return result


if __name__ == '__main__':
	url = 'https://codeforces.com/problemset/problem/1773/I'
	result = parse_problem(url)
	pp = pprint.PrettyPrinter()
	pp.pprint(result)

