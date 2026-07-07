from dataclasses import dataclass
import wjmanage.money as money
import wjmanage.date as date
import sqlite3
import random


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
        unit_value: money.Money - How much one of the item cost when purchased
    '''

    index: int
    name: str
    quantity: int
    unit_value: money.Money


@dataclass
class FinanceAccount:
    '''
    An account to perform transactions on

    Parameters:
        index: int - The ID/index of the account
        name: str - The name of the account
        currency: str - The currency of all the account's transactions
        balance: money.Money - The current calculated balance of the account
    '''

    index: int
    name: str
    currency: str
    balace: money.Money

@dataclass
class Transaction:
    '''
    A financial transaction

    Parameters:
        index: int - The ID/index of the transaction
        account: FinanceAccount - The account that the transaction took place in
        item: InventoryItem|None - The item that this transaction affects
        quantity: int - The quantity that the transaction contributes to the inventory
        description: str - The description of the transaction
        amount: money.Money - The amount of the transaction
        data: date.Date - The date that the transaction took place
    '''

    index: int
    account: FinanceAccount
    item: InventoryItem|None
    quantity: int
    description: str
    amount: money.Money
    date: date.Date

def _sql_sanitize(text: str) -> None:
    return text.replace("'", "''")


class DatabaseConnection:
    '''
    The central class for managing the database; essentially a wrapper around sqlite3.
    Connections are closed when the object is deleted, or can be closed manually.
    '''

    def __init__(self, filename: str) -> None:
        '''
        Initialize a connection to the main database.

        Parameters:
            filename: str - The path to the database file
        Returns:
            None
        '''
        self._con = sqlite3.connect(filename)
        self._cur = self._con.cursor()
        self._init_tables()

    def _init_tables(self) -> None:
        '''
        Initialize empty sqlite tables if none exist

        Returns:
            None
        '''

        table_defs = {
            "transactions": ["id", "account_id", "item_id", "quantity", "description", "amount", "year", "month", "day"],
            "accounts": ["id", "name", "currency", "balance"],
            "inventory": ["id", "name", "quantity", "currency", "unit_value"],
            "employees": ["id", "username", "name", "email", "position", "salt", "password_hash", "permissions", "year", "month", "day"]
        }
        for table_name in table_defs:
            self._cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name}({', '.join(table_defs[table_name])})"
            )
        self._con.commit()

    def _table_insert(self, table_name: str, values: list) -> None:
        '''
        Inserts a list of values into an sqlite3 table of a given name
        The table must already exist.

        Parameters:
            table_name: str - The table to insert into
            values: list - A list of values that correspond to the table's columns
        Returns:
            None
        '''

        self._cur.execute(
            f"INSERT INTO {table_name} VALUES({', '.join([str(i) for i in values])})"
        )
        self._con.commit()

    def _table_get(self, table_name: str, key: str, value: str):
        res = self._cur.execute(f"SELECT * FROM {table_name} WHERE {key}={value}")
        return res.fetchone()

    def _table_getall(self, table_name: str):
        res = self._cur.execute(f"SELECT * FROM {table_name}")
        return res.fetchall()

    def _list_to_transaction(self, response_list: list) -> Transaction:
        account = self.get_account_by_id(response_list[1])
        return Transaction(
            response_list[0],
            account,
            self.get_item_by_id(response_list[2]),
            response_list[3],
            response_list[4],
            money.Money(response_list[5], account.currency),
            date.Date(response_list[6], response_list[7], response_list[8])
        )
    def _list_to_account(self, response_list: list) -> FinanceAccount:
        return FinanceAccount(
            response_list[0],
            response_list[1],
            response_list[2],
            money.Money(response_list[3], response_list[2])
        )

    def get_account_by_id(self, index: int) -> FinanceAccount|None:
        response = self._table_get("accounts", "id", index)
        if not response:
            return None
        return self._list_to_account(response)

    def get_transaction_by_id(self, index: int) -> Transaction|None:
        response = self._table_get("transactions", "id", index)
        if not response:
            return None
        return self._list_to_transaction(response)


    def add_transaction(self, transaction: Transaction) -> bool:
        '''
        Adds a new transaction into the database.
        Will do nothing and return True if a transaction with the same ID already exists.

        Parameters:
            transaction: Transaction - the transaction to add
        Returns:
            bool - True of the transaction already exists with the same ID otherwise False
        '''

        self._table_insert("transactions",[
            transaction.index,
            transaction.account.index,
            0 if (transaction.item is None) else transaction.item.index,
            transaction.quantity,
            transaction.description,
            transaction.amount.get_value_cents(),
            transaction.date.year,
            transaction.date.month,
            transaction.date.day
        ])
        return False

    def close(self) -> None:
        '''
        Manually close the connection to the database.
        Nothing happens if it is already closed.

        Returns:
            None
        '''

        if self._con is not None:
            self._con.close()
        self._con = None

    def __del__(self) -> None:
        '''
        Automatically close the connection to the database.
        Nothing happens if it is already closed.

        Returns:
            None
        '''

        self.close()
