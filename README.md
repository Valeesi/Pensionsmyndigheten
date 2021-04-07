# Finding archived files
This script lists files - in directory X and not its sub directories - that have not been modified in the last Y days, i.e. older than Y days. The directory and days should be passed to the script as mandatory arguments. Written with `Python3`.

## Usage
Required arguments: 

`-p` for directory path and `-d` for number of days as input.


`-h` or `--help` for more information.
```shellscript
foo@bar:~$ python3 pm.py -p /path/to/directory -d 10
```

Example output:
```
./README.txt                          2019-05-09  17:19:53.193771720  +0200

./README.txt.gpg                      2019-05-09  17:20:21.331833720  +0200

./migratemost-master.zip              2019-05-20  12:52:34.867119547  +0200

./INC177759                           2019-05-23  13:29:47.014557386  +0200
```
