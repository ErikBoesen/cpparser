#!/usr/bin/env python3

from openpyxl import load_workbook
import argparse
import json

# TODO: shouldn't be named as a constant
NUMBER_COLUMN_OPTIONS = ('Team #', 'Team')
SCORE_COLUMN_OPTIONS = ('Cumulative Score')

parser = argparse.ArgumentParser(description='extract important information from CyberPatriot score dumps.')
parser.add_argument('file', help='name of/path to spreadsheet for parsing (typically in XLSX format)')
parser.add_argument('--teams', dest='teams', nargs='+', help='names of teams to focus on')
args = parser.parse_args()

wb = load_workbook(filename=args.file, read_only=True, data_only=True)
ws = wb.active

rows = ws.rows

def clean(string: str) -> str:
    """
    Trim trailing space from the end of field names.

    Some field headers have spaces appended to the end of the cells.
    """
    return string.strip()
fields = []
teams = []
for row in rows:
    row = [cell for cell in row if cell.value is not None]
    if row:
        if not fields:  # if fields have not yet been determined
            if row[0].value in NUMBER_COLUMN_OPTIONS:
                # This is the header row; make list of numbers
                fields = [clean(cell.value) for cell in row if cell.value is not None]
                # Store title of team number column
                number_column = fields[0]
                # Store title of total score column
                for field in fields:
                    if field in SCORE_COLUMN_OPTIONS:
                        score_column = field
        elif row[0].value is not None:  # skip any empty lines, otherwise store this team's data
            teams.append({fields[col]: cell.value for col, cell in enumerate(row)})

# Filter out teams with scores "Withheld" and similar messages.
# Sort in order of total score.
teams.sort(key=lambda team: team[score_column], reverse=True)

# Create a list of teams on which we desire to log data
select_teams = [team for team in teams if team[number_column] in args.teams] if args.teams else teams

with open('team_names.json', 'r') as f:
    team_names = json.load(f)

state_teams = {}
irrelevant = [number_column, 'Division', 'Location']
for team in select_teams:
    number = team[number_column]
    name = team_names.get(number)
    location = team['Location']
    print('Team {number}{name}:'.format(number=number,
                                        name=', ' + name if name else ''))
    for field in fields:
        if field not in irrelevant:
            value = team.get(field)
            # Print field and value, truncating floating point number if necessary
            print('\t{title}: {value}'.format(title=field.strip(),
                                              value=round(value, 8) if type(value) == float else value))
    # Build list of teams in this state or province to score from.
    if not state_teams.get(location):
        state_teams[location] = [opponent for opponent in teams if opponent['Location'] == location]
    print('\tWorld Rank: #{rank} of {total} teams'.format(rank=teams.index(team) + 1, total=len(teams)))
    print('\tState Rank: #{state_rank} of {state_total} teams'.format(state_rank=state_teams[location].index(team) + 1, state_total=len(state_teams[location])))
