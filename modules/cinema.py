import datetime
import re
import requests
from bs4 import BeautifulSoup
from data import urls

date = datetime.datetime.now().day
url = urls['dmik']

def get_html():
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    calendar = soup.find('div', class_='panel_block').find('div', id='calend')
    day = calendar.find('td', id="CalendTD{}".format(date)).find('a')
    soup = BeautifulSoup(str(day), features="lxml")
    info = [tag.attrs for tag in soup.findAll('a')]
    info = info[0]['title'].replace('<br>', ',\n').replace('МЗ', 'Малый зал').replace('БЗ', 'Большой зал').replace('D', 'Д')
    return info


get_page_data(get_html())