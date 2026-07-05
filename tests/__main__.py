import unittest
from wjmanage.money import Money

class MoneyTest(unittest.TestCase):
    def test_init(self):
        m = Money(1234, 'usd')
        self.assertEqual(m._value, 1234)
        self.assertEqual(m._currency, 'USD')
        with self.assertRaises(TypeError):
            Money(12.34, 'usd')

    def test_get_value(self):
        m = Money(1234, 'usd')
        self.assertEqual(m.get_value_cents(), 1234)

    def test_get_currency(self):
        m = Money(1234, 'usd')
        self.assertEqual(m.get_currency(), 'USD')

    def test_set_value(self):
        m = Money(1234, 'usd')
        m.set_value(5678)
        self.assertEqual(m._value, 5678)
        with self.assertRaises(TypeError):
            m.set_value(56.78)

    def test_set_currency(self):
        m = Money(1234, 'usd')
        m.set_currency('gbp')
        self.assertEqual(m._currency, 'GBP')

    def test_repr(self):
        m = f"{Money(1234, 'usd')}"
        self.assertEqual(m, '12.34 (USD)')

    def test_add(self):
        sm = Money(1234, 'usd') + Money(5678, 'usd')
        self.assertEqual(
            sm._value, 6912
        )
        with self.assertRaises(TypeError):
            sm + Money(1234, 'eur')

    def test_sub(self):
        sm = Money(1234, 'usd') - Money(5678, 'usd')
        self.assertEqual(
            sm._value, -4444
        )
        with self.assertRaises(TypeError):
            sm - Money(1234, 'eur')

    def test_mul(self):
        pd = Money(1234, 'usd') * 2
        self.assertEqual(pd._value, 2468)
        with self.assertRaises(TypeError):
            pd * 2.1

    def test_div(self):
        qt = Money(1234, 'usd') // 2
        self.assertEqual(qt._value, 617)
        with self.assertRaises(TypeError):
            qt // 2.1

    def test_percent(self):
        pc = Money(1234, 'usd').percent(12)
        self.assertEqual(pc._value, 148)
        with self.assertRaises(TypeError):
            pc.percent(0.5)

    def test_eq(self):
        self.assertTrue(
            Money(12, 'usd') == Money(12, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') == Money(13, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') == Money(12, 'gbp')

    def test_ne(self):
        self.assertTrue(
            Money(12, 'usd') != Money(13, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') != Money(12, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') != Money(12, 'gbp')

    def test_gt(self):
        self.assertTrue(
            Money(13, 'usd') > Money(10, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') > Money(12, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') > Money(20, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') > Money(11, 'gbp')

    def test_lt(self):
        self.assertTrue(
            Money(10, 'usd') < Money(13, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') < Money(12, 'usd')
        )
        self.assertFalse(
            Money(20, 'usd') < Money(12, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') < Money(11, 'gbp')

    def test_le(self):
        self.assertTrue(
            Money(10, 'usd') <= Money(13, 'usd')
        )
        self.assertTrue(
            Money(12, 'usd') <= Money(12, 'usd')
        )
        self.assertFalse(
            Money(20, 'usd') <= Money(12, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') <= Money(11, 'gbp')

    def test_ge(self):
        self.assertTrue(
            Money(13, 'usd') >= Money(10, 'usd')
        )
        self.assertTrue(
            Money(12, 'usd') >= Money(12, 'usd')
        )
        self.assertFalse(
            Money(12, 'usd') >= Money(20, 'usd')
        )
        with self.assertRaises(TypeError):
            Money(12, 'usd') >= Money(11, 'gbp')

    def test_iadd(self):
        m = Money(1234, 'usd')
        m += Money(21, 'usd')
        self.assertEqual(m._value, 1255)
        with self.assertRaises(TypeError):
            m += Money(1234, 'gbp')

    def test_isub(self):
        m = Money(1234, 'usd')
        m -= Money(21, 'usd')
        self.assertEqual(m._value, 1213)
        with self.assertRaises(TypeError):
            m -= Money(1234, 'gbp')

    def test_imul(self):
        m = Money(1234, 'usd')
        m *= 2
        self.assertEqual(m._value, 2468)
        with self.assertRaises(TypeError):
            m *= 2.1

    def test_ifloordiv(self):
        m = Money(1234, 'usd')
        m //= 2
        self.assertEqual(m._value, 617)
        with self.assertRaises(TypeError):
            m //= 2.1

    def test_neg(self):
        m = Money(1234, 'usd')
        m = -m
        self.assertEqual(m._value, -1234)


unittest.main()
