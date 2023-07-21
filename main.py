from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict


def calculate_years_passed(starting_year):
    age = datetime.datetime.now().year - starting_year
    if 11 <= age <= 14:
        year_ending = 'лет'
    elif age % 10 == 1:
        year_ending = 'год'
    elif 2 <= age % 10 <= 4:
        year_ending = 'года'
    elif 5 <= age % 10 <= 9 or age % 10 == 0:
        year_ending = 'лет'
    else:
        year_ending = 'Некорректная дата'
    return f"{age} {year_ending}"


excel_data = pandas.read_excel('wine3.xlsx')
excel_data.fillna('', inplace=True)
wine_dict = defaultdict(list)
for row in excel_data.to_dict(orient='records'):
    category = row['Категория']
    del row['Категория']
    wine_dict[category].append(row)
wine_dict = dict(wine_dict)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')
rendered_page = template.render(
    age=calculate_years_passed(1920),
    wines=wine_dict
)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
