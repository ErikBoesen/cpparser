#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse

URL = 'http://www.uscyberpatriot.org/competition/current-competition/scores'

#raw = requests.get(URL).content
raw = open('test_data/Scores.html').read()
# BeautifulSoup is actually a god-breathed piece of software
# Also it's 22:48 right now
# Send help
soup = BeautifulSoup(raw, 'html.parser')
main_list = soup.find('ul', class_='dfwp-column dfwp-list')
rounds = {
    rnd.find('div', class_='groupheader item medium').text: {
        lnk.text: lnk['href'] for lnk in rnd.find_all('a')
    } for rnd in main_list.find_all('li', class_='dfwp-item', recursive=False)
}
