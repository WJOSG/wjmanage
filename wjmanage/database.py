from dataclasses import dataclass
import money
import date

@dataclass
class Permissions:
    '''
    A set of permissions which determine what actions
    users are permitted to do

    Parameters:
        create_transactions: bool - Can the user create new transactions
        delete_transactions: bool - Can the user delete/modify transactions
        create_inventory: bool - Can the user create/modify inventory items
        delete_inventory: bool - Can the user delete inventory items
        manage_employees: bool - Can the user create/modify/delete employees
    '''

    create_transactions: bool
    delete_transactions: bool
    create_inventory: bool
    delete_inventory: bool
    manage_employees: bool

@dataclass
class Employee:
    '''
    An employee/user that is stored in the database

    Parameters:
        index: int - The ID/index of the employee in the database
        username: str - The login username of the employee
        name: str - The full name of the employee
        email: str - The employee's email address
        position: str - The employee's position eg. manager, sales, ...
        salt: str - A random string appended to the password when hashing
        password_hash: str - The hash of the user's password appended with the salt
        permissions: Permissions - A set of permissions for the employee
        start_date: date.Date - The date at which the employee started at the firm
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
    An item in the inventory database

    Parameters:
        index: int - The ID/index of the item
        name: str - The name of the item
        quantity: str - How many of the item exist
        unit_price: money.Money - How much one of the item costs if sold
        unit_value: money.Money - How much one of the item cost when purchased
    '''

    index: int
    name: str
    quantity: int
    unit_price: money.Money
    unit_value: money.Money

@dataclass
class Transaction:
    '''
    A financial transaction

    Parameters:
        index: int - The ID/index of the transaction
        description: str - The description of the transaction
        value: money.Money - The amount of the transaction
        data: date.Date - The date that the transaction took place
    '''

    index: int
    description: str
    value: money.Money
    date: date.Date

@dataclass
class FinanceAccount:
    '''
    An account to perform transactions on

    Parameters:
        index: int - The ID/index of the account
        name: str - The name of the account
        currency: str - The currency of all the account's transactions
    '''

    index: int
    name: str
    currency: str

class Database:
    '''
    '''

    def __init__(self) -> None:
        '''
        '''
        pass
