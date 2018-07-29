#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pick import pick

SCORE_PAGE = 'http://www.uscyberpatriot.org/competition/current-competition/scores'
OUTPUT_DIR = '/tmp/'

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
# TODO: Asegurar que no sea de forma PDF
url = rounds[chosen_round][chosen_division]
# TODO: There's likely a better way (read: an existing method) to remove the space escape codes.
spreadsheet = OUTPUT_DIR + url.split('/')[-1].replace('%20', ' ')
print('Saving ' + spreadsheet)
# TODO: Check if requests has a better method for downloading files
with open(spreadsheet, 'w') as f:
    f.write(requests.get(url).content.decode())
