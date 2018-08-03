#!/usr/bin/env python3

from openpyxl import load_workbook
import argparse
import json

parser = argparse.ArgumentParser(description='extract important information from CyberPatriot score dumps.')
parser.add_argument('file', help='name of/path to spreadsheet for parsing (typically in XLSX format)')
parser.add_argument('--teams', dest='teams', nargs='+', help='names of teams to focus on')
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

# Filter out teams with scores "Withheld" and similar messages.
teams = [team for team in teams if type(team['Cumulative Score']) in (int, float)]
# Sort in order of total score.
teams.sort(key=lambda team: team['Cumulative Score'], reverse=True)

# Create a list of teams on which we desire to log data
select_teams = [team for team in team if team['Team #'] in args.teams] if args.teams else teams

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
    # TODO: Improve efficiency.
    state_teams = [opponent for opponent in teams if opponent['Location'] == team['Location']]
    print('\tWorld Rank: #{rank} of {total} teams'.format(rank=teams.index(team) + 1, total=len(teams)))
    print('\tState Rank: #{state_rank} of {state_total} teams'.format(state_rank=state_teams.index(team) + 1, state_total=len(state_teams)))
