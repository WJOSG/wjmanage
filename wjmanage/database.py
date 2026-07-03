from dataclasses import dataclass
import money
import date

@dataclass
class Permissions:
    '''
    '''

    create_transactions: bool
    delete_transactions: bool
    create_inventory: bool
    delete_inventory: bool
    manage_employees: bool

@dataclass
class Employee:
    '''
    '''

    index: int
    username: str
    name: str
    email: str
    position: str
    salt: str
    password_hash: str
    permissions: Permissions
    start_date: date.Date



@dataclass
class InventoryItem:
    '''
    '''

    index: int
    name: str
    quantity: int
    unit_price: int

@dataclass
class Transaction:
    '''
    '''

    index: int
    description: str
    value: money.Money
    date: date.Date

@dataclass
class FinanceAccount:
    '''
    '''

    index: int
    name: str
    currency: str

class Database:
    '''
    '''

    def __init__(self):
        '''
        '''
        pass
