#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pick import pick
from urllib.parse import unquote
import argparse

parser = argparse.ArgumentParser(description='efficiently download CyberPatriot score spreadsheets.')
parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='fetch from a score page stored in the WayBack machine; useful for offseason testing')
args = parser.parse_args()

SCORE_PAGE = 'http://www.uscyberpatriot.org/competition/current-competition/scores'
DEBUG_PAGE = 'http://web.archive.org/web/20180328102148/http://www.uscyberpatriot.org/competition/current-competition/scores'
OUTPUT_DIR = '/tmp/'

page = requests.get(DEBUG_PAGE if args.debug else SCORE_PAGE).content
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
