# Pensionsmyndigheten's test
The test requires development of a script which is able to probe a directory for files that have not been modified in the last X days. It requires the output to be consistd of names of eligible files sorted by their modified times. The solution is given preemptively (due to security concerns) below in the form of a markdown document oppose to the actual scripts. 

## Original problem description
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
## Main Script
```Python
#!/usr/bin/python3

import argparse
import datetime
import sys
import os


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Find unmodified files in a directory")
    parser.add_argument("-i", '--include_hidden', action='store_true', help="Include hidden files")
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument("-p", '--path', type=str, metavar='', required=True, help="Target directory")
    required_args.add_argument("-d", '--days', type=str, metavar='', required=True,
                               help="Days without modification, maximum 50 years")
    return parser


def get_number_of_days(days):
    try:
        days = int(days)
        if 0 > days or days > 365 * 50:
            sys.exit("Invalid input. Number of days must be a natural number between 0 and 18250 (50 years)")
        else:
            return days
    except ValueError as err:
        sys.exit("ValueError: " + str(err))


def check_if_dir_valid(path):
    if not os.path.isdir(path):
        sys.exit("-p must be a valid directory path.")
    else:
        return True


def get_cutoff_time_from_now(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)


def get_all_files_from_path(path):
    return filter(os.path.isfile, os.listdir(path))


def sort_files_by_mtime(files, include_hidden):
    return sorted((include_hidden and files) or [i for i in files if not i.startswith(".")], key=os.path.getmtime)


def get_maximum_filename_length(files, path):
    return str(max(map(len, files)) + len(path))


def get_output_format(sorted_files, path):
    return "{:" + get_maximum_filename_length(sorted_files, path) + "s} {:30s}"


def print_files_with_mtime(files, output_column_space):
    for f in files:
        print(output_column_space.format(f, datetime.datetime.strftime(get_mtime_from_file(f),
                                                                       "%Y-%m-%d %H:%M:%S.%f")))


def get_mtime_from_file(f):
    return datetime.datetime.fromtimestamp(os.stat(f).st_mtime)


def get_files_before_cutoff_time(files, cutoff_time):
    return list(filter(
        lambda f: get_mtime_from_file(f) <= cutoff_time, files))


def print_files_by_mtime(path, cutoff_time, include_hidden):
    check_if_dir_valid(path)

    os.chdir(path)
    files = get_all_files_from_path(path)
    files_before_cutoff_time = get_files_before_cutoff_time(files, cutoff_time)

    if len(files_before_cutoff_time) == 0:
        print("No search results.")
        exit(0)
    else:
        sorted_files = sort_files_by_mtime(files_before_cutoff_time, include_hidden)
        output_format = get_output_format(sorted_files, path)
        print_files_with_mtime(sorted_files, output_format)


if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    cutoff = get_cutoff_time_from_now(get_number_of_days(args.days))
    print_files_by_mtime(args.path, cutoff, args.include_hidden)

```

## Example test cases
It requires [pyfakefs](https://pypi.org/project/pyfakefs/) (a library for mocking file systems) to run. Duo to time constraints, only some example test cases are showcased.
```Python
#!/usr/bin/python3
from unittest import mock

import pm
import os
import unittest
import datetime

from pyfakefs.fake_filesystem_unittest import TestCase

invalid_days_range_error = "Invalid input. Number of days must be a natural number between 0 and 18250 (50 years)"
invalid_days_value_error = "ValueError: invalid literal for int() with base 10:"
invalid_path_error = "-p must be a valid directory path."


class TestPM(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_check_if_days_valid(self):
        self.assertEqual(9999, pm.get_number_of_days(9999))

    def test_check_if_days_valid_greater(self):
        with self.assertRaises(SystemExit) as cm:
            pm.get_number_of_days(18251)
        self.assertEqual(cm.exception.code, invalid_days_range_error)

    def test_check_if_days_valid_less(self):
        with self.assertRaises(SystemExit) as cm:
            pm.get_number_of_days(-1)
        self.assertEqual(cm.exception.code, invalid_days_range_error)

    def test_check_if_days_valid_using_letters(self):
        with self.assertRaises(SystemExit) as cm:
            pm.get_number_of_days("pension")
        self.assertTrue(invalid_days_value_error in cm.exception.code)

    def test_check_if_days_valid_empty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.get_number_of_days("")
        self.assertTrue(invalid_days_value_error in cm.exception.code)

    def test_check_if_dir_valid_empty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_dir_valid("")
        self.assertTrue(invalid_path_error in cm.exception.code)

    def test_check_if_dir_valid_faulty(self):
        dir_path = '/pension'
        file_path = '/pension/file.txt'

        with self.assertRaises(SystemExit) as cm:
            pm.check_if_dir_valid(dir_path)
        self.assertTrue(invalid_path_error in cm.exception.code)
        self.fs.create_file(file_path)
        self.assertTrue(pm.check_if_dir_valid(dir_path))

    @mock.patch('builtins.print')
    def test_get_files_before_cutoff_time(self, mock_print):
        dir_path = '/integration'
        file_path = ['/integration/file_today.txt',
                     '/integration/file_yesterday.txt',
                     '/integration/another_folder/file_whatever.txt']

        mtime = datetime.datetime(2010, 10, 10, 0, 0, 0)
        for path in file_path:
            self.fs.create_file(path)
            set_file_modification_time(path, mtime)
            mtime -= datetime.timedelta(days=1)

        test_time_1 = datetime.datetime(2010, 10, 10, 0, 0, 1)
        pm.print_files_by_mtime(dir_path, test_time_1, False)
        self.assertEqual(2, len(pm.get_files_before_cutoff_time(pm.get_all_files_from_path(dir_path),
                                                                test_time_1)))
        test_time_2 = datetime.datetime(2010, 10, 9, 23, 59, 59)
        pm.print_files_by_mtime(dir_path, test_time_2, False)
        self.assertEqual(1, len(pm.get_files_before_cutoff_time(pm.get_all_files_from_path(dir_path),
                                                                test_time_2)))


def set_file_modification_time(filename, mtime):
    os.utime(filename, times=(os.stat(filename).st_atime, mtime.timestamp()))


if __name__ == '__main__':
    unittest.main()

```

## Compatibility
The script was written in Python 3.8.6, tested on Windows 10 and Ubuntu 18.08.
