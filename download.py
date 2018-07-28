#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pick import pick

SOURCE = 'http://www.uscyberpatriot.org/competition/current-competition/scores'
OUTPUT_DIR = '/tmp'

#raw = requests.get(SOURCE).content
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

rnd = pick(list(rounds.keys()), title='Pick a round to get data on.')[0]
div = pick(list(rounds[rnd].keys()), title='Pick a division to get data on.')[0]
url = rounds[rnd][div]
# TODO: There's likely a better way (read: an existing method) to remove the space escape codes.
outfile = url.split('/')[-1].replace('%20', ' ')
print('Downloading ' + outfile + ' from ' + url)
# TODO: Check if requests has a better method for downloading files
with open(OUTPUT_DIR + '/' + outfile, 'w') as f:
    f.write(requests.get(url).content)
