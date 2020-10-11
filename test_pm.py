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
