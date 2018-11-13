import unittest
from CodingPractice.PythonAssignments.cleancode.DateUtils import workdays_in_range


class DateCalculatorTests(unittest.TestCase):

    def test_00_number_of_days_between(self):
        start = '2018/11/09'
        end = '2018/11/30'
        self.assertEqual(15, workdays_in_range(start, end))

    def test_01_same_day(self):
        start = '2018/11/09'
        end = '2018/11/09'
        self.assertEqual(0, workdays_in_range(start, end))

    def test_02_one_week_count(self):
        start = '2018/11/12'
        end = '2018/11/19'
        self.assertEqual(5, workdays_in_range(start, end))

    


if __name__ == '__main__':
    unittest.main()
