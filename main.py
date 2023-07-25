from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import os
from dotenv import load_dotenv
from collections import defaultdict


def calculate_years_passed(starting_year):
    age = datetime.datetime.now().year - starting_year
    ending = determine_the_age_ending(age)
    return f'{age} {ending}'


def determine_the_age_ending(age):
    if 11 <= age <= 14 or 5 <= age % 10 <= 9 or age % 10 == 0:
        year_ending = 'лет'
    elif age % 10 == 1:
        year_ending = 'год'
    elif 2 <= age % 10 <= 4:
        year_ending = 'года'
    else:
        return 'Некорректная дата'
    return year_ending


def load_excel_data(file_path):
    excel_data = pandas.read_excel(file_path)
    excel_data.fillna('', inplace=True)
    wines = defaultdict(list)
    for row in excel_data.to_dict(orient='records'):
        category = row.pop('Категория')
        wines[category].append(row)
    return wines


def render_template(data):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    return template.render(data)

def save_to_html(html_content, output_file):
    with open(output_file, 'w', encoding="utf8") as file:
        file.write(html_content)

def start_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

def main():
    load_dotenv()
    starting_year = 1920
    age_data = calculate_years_passed(starting_year)
    excel_file_path = os.getenv('EXCEL_FILE_PATH')
    wine_data = load_excel_data(excel_file_path)
    data_to_render = {
        'age': age_data,
        'wines': wine_data
    }
    rendered_page = render_template(data_to_render)
    output_html_file = 'index.html'
    save_to_html(rendered_page, output_html_file)
    start_server()

if __name__ == '__main__':
    main()