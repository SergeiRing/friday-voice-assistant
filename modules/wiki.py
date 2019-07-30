import requests
import re
from bs4 import BeautifulSoup
from data import urls


def urlgen(query):
    url = urls['wikipedia'].format(query)
    return url

def get_link(url):
    rjson = requests.get(url).json()
    #print(rjson)
    links = rjson[3]
    return links

def get_info(links):
    info = ''
    articles = {}
    for link in links:
        cleantext = ''
        r = requests.get(link).text
        soup = BeautifulSoup(r, 'lxml')
        block = soup.find('div', id = 'content').find('div', id='bodyContent').find_all('p')
        title = soup.find('h1', id = 'firstHeading')
        for item in block:
            cleanr = re.compile('<.*?>')
            cleantext += re.sub(cleanr, '', str(item))
        cleantext = cleantext[0:500]
        title = str(re.sub(re.compile('<.*?>'), '', str(title)))
        articles[title] = [cleantext]
        articles[title].append(link)
    return articles
