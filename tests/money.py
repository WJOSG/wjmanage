from wjmanage.money import Money
import unittest

class MoneyTest(unittest.TestCase):
    def test_init(self):
        m = Money(1234, 'usd')
        self.assertEqual(m._value, 1234, 'Value incorrectly initialized.')
        self.assertEqual(m._currency, 'USD', 'Currency incorrectly initialized.')

