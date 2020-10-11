#!/usr/bin/python3


import unittest.mock
import pm

invalid_days_range_error = "Invalid input. Number of days must be a natural number between 0 and 18250 (50 years)"
invalid_days_value_error = "ValueError: invalid literal for int() with base 10:"


class TestPM(unittest.TestCase):
    def test_check_if_days_valid_greater(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_days_valid(18251)
        self.assertEqual(cm.exception.code, invalid_days_range_error)

    def test_check_if_days_valid_less(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_days_valid(-1)
        self.assertEqual(cm.exception.code, invalid_days_range_error)

    def test_check_if_days_valid_using_letters(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_days_valid("hellokitty")
        self.assertTrue(invalid_days_value_error in cm.exception.code)

    def test_check_if_days_valid_empty(self):
        with self.assertRaises(SystemExit) as cm:
            pm.check_if_days_valid("")
        self.assertTrue(invalid_days_value_error in cm.exception.code)


if __name__ == '__main__':
    unittest.main()
