#!/usr/bin/python3


import unittest.mock
import pm

invalid_days_range_error = "Invalid input. Number of days must be a natural number between 0 and 18250 (50 years)"
invalid_days_value_error = "ValueError: invalid literal for int() with base 10:"
invalid_path_error = "-p must be a valid directory path."


class TestPM(unittest.TestCase):
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
            pm.get_number_of_days("hellokitty")
        self.assertTrue(invalid_days_value_error in cm.exception.code)

    def test_check_if_days_valid_empty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.get_number_of_days("")
        self.assertTrue(invalid_days_value_error in cm.exception.code)

    def test_check_if_path_valid_empty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_path_valid("")
        self.assertTrue(invalid_path_error in cm.exception.code)

    def test_check_if_path_valid_faulty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_path_valid("PP:/Downasdasd")
        self.assertTrue(invalid_path_error in cm.exception.code)


if __name__ == '__main__':
    unittest.main()
