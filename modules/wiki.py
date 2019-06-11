import requests
import re
from bs4 import BeautifulSoup

#url = 'https://ru.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&srsearch=ван гог&format=json'

def urlgen(query):
    url = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search={}&limit=3&format=json'.format(query)
    return url

def get_link(url):
    rjson = requests.get(url).json()
    #print(rjson)
    links = rjson[3]
    return links

def get_info(links):
    info = ''
    for link in links:
        cleantext = ''
        r = requests.get(link).text
        soup = BeautifulSoup(r, 'lxml')
        block = soup.find('div', id='content').find('div', id='bodyContent').find_all('p')
        for item in block:
            cleanr = re.compile('<.*?>')
            cleantext += re.sub(cleanr, '', str(item))
        cleantext = cleantext[0:500]
        info += cleantext
        info += '\n'
        info += link
        info += '\n\n'
    return info