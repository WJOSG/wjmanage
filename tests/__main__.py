import unittest
from tests.money import *
from tests.date import *

unittest.main()

from wjmanage.database import DatabaseConnection, Transaction, FinanceAccount
from wjmanage.money import Money
from wjmanage.date import Date

db = DatabaseConnection("test.db")
