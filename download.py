#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pick import pick
from urllib.parse import unquote

SCORE_PAGE = 'http://www.uscyberpatriot.org/competition/current-competition/scores'
OUTPUT_DIR = '/tmp/'

# TODO: NO DEBUG
#page = requests.get(SOURCE).content
page = open('test_data/Scores.html').read()
soup = BeautifulSoup(page, 'html.parser')
main_list = soup.find('ul', class_='dfwp-column dfwp-list')
rounds = {
    rnd.find('div', class_='groupheader item medium').text: {
        lnk.text: lnk['href'] for lnk in rnd.find_all('a')
    } for rnd in main_list.find_all('li', class_='dfwp-item', recursive=False)
}

chosen_round    = pick(list(rounds.keys()), title='Pick a round to get data on.')[0]
chosen_division = pick(list(rounds[chosen_round].keys()), title='Pick a division to get data on.')[0]
uri = rounds[chosen_round][chosen_division]
spreadsheet = OUTPUT_DIR + unquote(uri.split('/')[-1])

print('URI: ' + uri)
print('Output: ' + spreadsheet)
open(spreadsheet, 'wb').write(requests.get(uri).content)
