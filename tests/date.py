import unittest
from wjmanage.date import Date

class DateTest(unittest.TestCase):
    def test_init(self):
        d = Date(2020, 12, 12)
        self.assertEqual(d.year, 2020)
        self.assertEqual(d.month, 12)
        self.assertEqual(d.day, 12)
        with self.assertRaises(ValueError):
            Date(2020, 21, 10)
        with self.assertRaises(ValueError):
            Date(2020, -2, 10)
        with self.assertRaises(ValueError):
            Date(2020, 1, 90)
        with self.assertRaises(ValueError):
            Date(2020, 1, -3)

    def test_repr(self):
        self.assertEqual(
            f"{Date(2032, 12, 5)}",
            "2032.12.05"
        )

