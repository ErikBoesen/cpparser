#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse

URL = 'http://www.uscyberpatriot.org/competition/current-competition/scores'

#raw = requests.get(URL).content
raw = open('test_data/Scores.html').read()
soup = BeautifulSoup(raw, 'html.parser')
print(soup.find_all('ul', class_='dfwp-column dfwp-list')[0].prettify())
