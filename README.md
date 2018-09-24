# cpparser
> A helpful set of utilities for downloading and processing CyberPatriot scoring data.

AFA releases CyberPatriot scores by posting Excel spreadsheets for each division of each round [on their website](http://www.uscyberpatriot.org/competition/current-competition/scores). This method is rather inconvenient for users, though it is understandable that the AFA would use it given the ease of storing an Excel spreadsheet as compared to hosting a full score database which may be more difficult to query than a spreadsheet. (An open format like CSV would be preferable, though, to an Excel spreadsheet...)

Dealing with this situation efficiently and with minimal headache is what `cpparser` does best. I created it in order to save myself time when posting summaries of performance for my school's CyberPatriot teams. This was previously a tedious process which required me to scroll through various spreadsheets, copy and paste from numerous cells, etc., so I decided to automate this process.

## Setup
All programs require Python 3 to be installed. Dependencies can be installed easily through `pip` as follows:
```sh
pip3 install -r requirements.txt
```
You may wish to append `--user` to that command to install only for your user account (no root privileges required).

## `download.py`
First, users can run `download.py`, either directly with `./download.py`, or through Python, i.e. `python3 download.py`. This program allows the user to choose which round and division's data they wish to query. This program will allow users to skip direct interaction with CyberPatriot's website. Why use a website when you can use the command line?

During the offseason period, CyberPatriot typically removes links to score spreadsheets from the website. If wishing to test the script, you may use the flag `--debug` to fetch a copy of the finishing CyberPatriot X score list through the Wayback Machine.

## `read.py`
This script allows for easy command-line reading of CyberPatriot formatted `xlsx` files. It's mainly for debugging, but may be useful for users who wish to read the spreadsheets but don't have or wish to open Excel.

## `parse.py`
This script, the most time-saving of the three, reads a given Excel spreadsheet and outputs a summary of the performance of one or more teams in various formats. This was originally the goal of `cpparser`.

Right now, the script will output team data in the following format:
```
Team __-____:
    Round 1 Score: ___
    Round 2 Network Security (Images): ___
    ...
```
All fields provided by the spreadsheet will be shown except those specifically excluded. This way, no information will be hidden which ought not be.

`parse.py` can be used as shown in the following example:
```sh
python3 parse.py spreadsheet_path.xlsx --teams 10-1018 10-1418 #...
```
You should add all teams on which you wish to get data following `--teams`.

Generally, all teams in a spreadsheet are from the same season of CyberPatriot. Thus, you can use this typical command-line shorthand (equivalent to the above command):
```sh
python3 parse.py spreadsheet_path.xlsx --teams 10-{1018,1418}
```

## Licensing & Authorship
This software was created by [Erik Boesen](https://github.com/ErikBoesen) and is provided under the [MIT License](LICENSE).
