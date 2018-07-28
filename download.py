#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse

URL = 'http://www.uscyberpatriot.org/competition/current-competition/scores'

#raw = requests.get(URL).content
raw = open('test_data/Scores.html').read()
soup = BeautifulSoup(raw, 'html.parser')
rounds = []
main_list = soup.find('ul', class_='dfwp-column dfwp-list')
print(len(main_list.find_all('li', class_='dfwp-item', recursive=False)))
for rnd in main_list.find_all('li', class_='dfwp-item', recursive=False):
    title = rnd.find('div', class_='groupheader item medium').text
    for lnk in rnd.find_all('a'):
        print('{name} /// {url}'.format(name=lnk.text, url=lnk['href']))
    print('-=' * 40)
