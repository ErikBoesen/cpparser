#!/usr/bin/env python3

from openpyxl import load_workbook
import argparse

parser = argparse.ArgumentParser(description='Read a CyberPatriot score spreadsheet.')
parser.add_argument('file', help='name of/path to spreadsheet for parsing (typically in XLSX format)')
args = parser.parse_args()

wb = load_workbook(filename=args.file, read_only=True)
ws = wb.active

rows = ws.rows

for row in rows:
    for cell in row:
        print(cell.value, end='\t')
    print()
