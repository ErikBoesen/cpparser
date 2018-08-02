#!/usr/bin/env python3

from openpyxl import load_workbook
import argparse
import json

parser = argparse.ArgumentParser(description='extract important information from CyberPatriot score dumps.')
parser.add_argument('file', help='name of/path to spreadsheet for parsing (typically in XLSX format)')
parser.add_argument('--teams', dest='teams', nargs='+', help='names of teams to focus on')
# TODO: Implement CSV support
#parser.add_argument('--csv', dest='csv', help='output data in CSV format')
args = parser.parse_args()

wb = load_workbook(filename=args.file, read_only=True, data_only=True)
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
            fields = [clean(cell.value) for cell in row]
    elif row[0].value is not None:
        teams.append({fields[col]: cell.value for col, cell in enumerate(row)})

if args.teams:
    select_teams = list(filter(lambda team: team['Team #'] in args.teams, teams))
else:
    select_teams = teams

# Filter out teams with scores "Withheld" and similar messages.
world_teams = list(filter(lambda team: type(team['Cumulative Score']) in (int, float), teams))
# Sort in order of total score.
world_teams = sorted(world_teams, key=lambda team: team['Cumulative Score'], reverse=True)
print([team['Cumulative Score'] for team in world_teams])

with open('team_names.json', 'r') as f:
    team_names = json.load(f)

irrelevant = ['Team #', 'Division', 'Location']
for team in select_teams:
    number = team['Team #']
    name = team_names.get(number)
    print('Team {number}{name}:'.format(number=number,
                                        name=', ' + name if name else ''))
    for field in fields:
        if field not in irrelevant:
            print('\t{title}: {value}'.format(title=field,
                                              value=team.get(field)))
    # TODO: Oh god this is inefficient.
    #state_teams = list(sorted(list(filter(lambda opponent: team['Location'] == opponent['Location'], teams)), key='Cumulative Score'))
    #print('\tWorld Rank: {world_rank}'.format(world_rank=world_teams.index(team)))  # TODO: Test
    #print('\tState Rank: {state_rank}'.format(state_rank=state_teams.index(team)))  # TODO: Same

# TODO: Currently ignores rankings.
