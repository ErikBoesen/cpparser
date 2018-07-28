#!/usr/bin/env python3

from openpyxl import load_workbook
import argparse

parser = argparse.ArgumentParser(description='extract important information from CyberPatriot score dumps.')
parser.add_argument('file', help='name of/path to spreadsheet for parsing (typically in XLSX format)')
parser.add_argument('--teams', dest='teams', nargs='+', help='names of teams to focus on')
# TODO: Implement CSV support
#parser.add_argument('--csv', dest='csv', help='output data in CSV format')
args = parser.parse_args()

wb = load_workbook(filename=args.file, read_only=True)
ws = wb.active

rows = ws.rows

def clean(string: str) -> str:
    return string[:-1] if string[-1] == ' ' else string

fields = []
teams = []
for row in rows:
    if not fields:  # if fields have not yet been determined
        if row[0].value == 'Team #':
            # This is the header row
            fields = [cell.value for cell in row]
    else:
        teams.append({fields[col]: cell.value for col, cell in enumerate(row)})

if args.teams:
    teams = list(filter(lambda team: team['Team #'] in args.teams, teams))

relevant = ['CCS Images ', 'Cisco Networking ', 'Cumulative Score']
for team in teams:
    print('Team {number}:'.format(number=team['Team #']))
    for field in relevant:
        print('\t{title}: {value}'.format(title=clean(field),
                                          value=team[field]))

# TODO: Currently ignores rankings.
