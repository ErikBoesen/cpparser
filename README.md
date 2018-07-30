# cpparser
> A helpful set of utilities for downloading and processing CyberPatriot scoring data.

AFA releases CyberPatriot scores by posting Excel spreadsheets for each division of each round [on their website](http://www.uscyberpatriot.org/competition/current-competition/scores). This method is rather inconvenient for users, though it is understandable that the AFA would use it given the ease of storing an Excel spreadsheet as compared to hosting a full score database which may be more difficult to query than a spreadsheet. (An open format like CSV would be preferable, though, to an Excel spreadsheet...)

Dealing with this situation efficiently and with minimal headache is what `cpparser` does best.

## Setup
All programs require Python 3 to be installed. Dependencies can be installed easily through `pip` as follows:
```sh
pip3 install -r requirements.txt
```
You may wish to append `--user` to that command to install only for your user account (no root privileges required).

## `download.py`
First, users can run `download.py`, either directly with `./download.py`, or through Python, i.e. `python3 download.py`. This program allows the user to choose which round and division's data they wish to query. This program will allow users to skip direct interaction with CyberPatriot's website. Why use a website when you can use the command line?

