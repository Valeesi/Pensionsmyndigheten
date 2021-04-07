## Problem description
```
Write a script (Bash, Python etc.) that checks for files - in directory X - that have not been modified in the last Y days, i.e. older than Y days.

The directory and days should be passed to the script as mandatory arguments.

The script shall only look for files in directory X, not in sub directories. You may assume that none of the filenames contain newlines.

The output of the script should print the file names, and the time for when the file was last modified, sorted by modification time.

See below for an example, your output can look different.

./README.txt                          2019-05-09  17:19:53.193771720  +0200

./README.txt.gpg                      2019-05-09  17:20:21.331833720  +0200

./migratemost-master.zip              2019-05-20  12:52:34.867119547  +0200

./INC177759                           2019-05-23  13:29:47.014557386  +0200

Include a help option, so that if '-h' or '--help' is passed as an optional argument, a summary of what the program does is printed to stdout.

Also try to handle user errors so the script exits gracefully with an error message upon incorrect - or missing - input.
```

## Usage
Required arguments: `-p` for directory path and `-d` for number of days as input.


`-h` or `--help` for more information.
```shellscript
foo@bar:~$ python3 pm.py -p /path/to/directory -d 10
```
## Compatibility
The script was written in Python 3.8.6, tested on Windows 10 and Ubuntu 18.08.
