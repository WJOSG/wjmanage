from dataclasses import dataclass
import wjmanage.money as money
import wjmanage.date as date
import sqlite3
import random
import secrets
import hashlib
import time

SESSION_TIME_SECONDS = 60 * 10


@dataclass
class Permissions:
    '''
    A set of permissions which determine what actions
    users are permitted to do

    Parameters:
        create_transactions (bool): Can the user create new transactions
        delete_transactions (bool): Can the user delete/modify transactions
        create_inventory (bool): Can the user create/modify inventory items
        delete_inventory (bool): Can the user delete inventory items
        manage_employees (bool): Can the user create/modify/delete employees
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
        index (int): The ID/index of the employee in the database
        username (str): The login username of the employee
        name (str): The full name of the employee
        email (str): The employee's email address
        position (str): The employee's position eg. manager, sales, ...
        salt (str): A random string appended to the password when hashing
        password_hash (str): The hash of the user's password appended with the salt
        permissions (Permissions): A set of permissions for the employee
        start_date (date.Date): The date at which the employee started at the firm
        auth (str): The employee's authentication token
        expires (int): Unix time for when the user's authentication expires
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
    auth: str
    expires: int



@dataclass
class InventoryItem:
    '''
    An item in the inventory database

    Parameters:
        index (int): The ID/index of the item
        name (str): The name of the item
        category (str): The item's category
        quantity (str): How many of the item exist
        unit_value (money.Money): How much one of the item cost when purchased
    '''

    index: int
    name: str
    category: str
    quantity: int
    unit_value: money.Money


@dataclass
class FinanceAccount:
    '''
    An account to perform transactions on

    Parameters:
        index (int): The ID/index of the account
        name (str): The name of the account
        category (str): The account's category
        currency (str): The currency of all the account's transactions
        balance (money.Money): The current calculated balance of the account
    '''

    index: int
    name: str
    category: str
    currency: str
    balace: money.Money

@dataclass
class Transaction:
    '''
    A financial transaction

    Parameters:
        index (int): The ID/index of the transaction
        account (FinanceAccount): The account that the transaction took place in
        category (str): The transaction's category
        item (InventoryItem|None): The item that this transaction affects
        quantity (int): The quantity that the transaction contributes to the inventory
        description (str): The description of the transaction
        amount (money.Money): The amount of the transaction
        data (date.Date): The date that the transaction took place
    '''

    index: int
    account: FinanceAccount
    category: str
    item: InventoryItem|None
    quantity: int
    description: str
    amount: money.Money
    date: date.Date

def _sql_sanitize(text: str)  None:
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
            filename (str): The path to the database file
        Returns:
            None
        '''
        self._con = sqlite3.connect(filename)
        self._cur = self._con.cursor()
        self._init_tables()

    def __del__(self) -> None:
        '''
        Automatically close the connection to the database.
        Nothing happens if it is already closed.

        Returns:
            None
        '''

        self.close()

    def authenticate_login(self, username: str, password: str) -> Employee|None:
        '''
        Authenticates an employee based on username and password login.

        Parameters:
            username (str): The login username
            password (str): The login password
        Returns:
            Employee|None: The authenticated employee or None if incorrect username or password
        
        '''
        response = self._table_get('employees', 'username', f"'{username}'")
        if response is None:
            return None
        user = self._list_to_employee(response)
        password_hash = hashlib.sha256((user.salt + password + user.salt).encode()).hexdigest()
        if password_hash != user.password_hash:
            return None
        new_auth = secrets.token_hex(32)
        new_expires = int(time.time() + SESSION_TIME_SECONDS)
        self._table_update('employees', 'username', f"'{username}'",
                           auth=f"'{new_auth}'",
                           expires=new_expires)
        response = self._table_get('employees', 'username', f"'{username}'")
        return self._list_to_employee(response)

    def authenticate_token(self, auth_token: str) -> Employee|None:
        '''
        Checks the validity if an authentication token and returns the
        corresponding employee if valid.

        Parameters:
            auth_token (str): The authentication token
        Returns:
            Employee|None: The corresponding employee or None if the auth token is invalid or expired
        '''
        response = self._table_get(self, 'auth', f"'{auth_token}'")
        if response is None:
            return None
        user = self._list_to_employee(response)
        if time.time() > user.expires:
            return None
        return user

    def create_employee(self, username: str, name: str, email: str, position: str,
                        password: str, permissions: Permissions, start_date: date.Date) -> None:
        '''
        Creates a new employee with a random ID, and creates a unique password hash and salt
        for the login account.

        Parameters:
            username (str): The employee's login username
            name (str): The employee's name
            email (str): The employee's email, does not check for validity
            position (str): The employee's job position
            password (str): The employee's login password
            permissions (Permissions): The employee's database access permissions
            start_date (date.Date): The date at which the employee started

        Returns:
            None

        '''
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256((salt + password + salt).encode()).hexdigest()
        employee = Employee(
            index = random.randint(999_999_999),
            username = username,
            name = name,
            email = email,
            position = position,
            salt = salt,
            password_hash = password_hash,
            permissions = permissions,
            start_date = start_date,
            auth = "",
            expires = 0
        )
        self._table_insert("employees", self._employee_to_list(account))

    def create_account(self, name: str, category: str, currency: str,
                       balance: money.Money) -> None:
        '''
        Creates a new account with a random ID and adds it to the database.

        Parameters:
            name (str): The name of the account
            category (str): The account's category
            currency (str): The currency of all the accounts transactions
            balance (money.Money): The current calculated balance of the account
        Returns:
            None
        '''
        account = FinanceAccount(
            index = random.randint(999_999_999),
            name = name,
            category = category,
            currency = currency,
            balance = balance
        )
        self._table_insert("accounts", self._account_to_list(account))

    def create_item(self, name: str, category: str, 
                    quantity: int, unit_value: money.Money) -> None:
        '''
        Creates a new inventory item and adds it to the database.

        Parameters:
            name (str): The name of the item
            category (str): The item's category
            quantity (str): How many of the item exist
            unit_value (money.Money): How much one of the item cost when purchased
        Returns:
            None
        '''
        item = InventoryItem(
            index = random.randint(999_999_999),
            name = name,
            category = category,
            quantity = quantity,
            unit_value = unit_value
        )
        self._table_insert("inventory", self._item_to_list(item))

    def create_transaction(self, account: FinanceAccount,
                           category: str, item: InventoryItem|None,
                           quantity: int, description: str, amount: money.Money,
                           date: date.Date) -> None:
        '''
        Creates a new transaction with random ID and adds it to the database.

        Parameters:
            account (FinanceAccount): The account which the transaction belongs to
            category (str): The transaction's category
            item (InventoryItem|None): The item that the transaction affects
            quantity (int): The quantity that the transaction contributes to the inventory
            description (str): The description of the transaction
            amount (money.Money): The amount of the transaction
            date (date.Date): The date that the transaction took place
        Returns:
            None
        '''
        transaction = Transaction(
            index = random.randint(999_999_999),
            account = account,
            category = category,
            item = item,
            quantity = quantity,
            description = description,
            amount = amount,
            date = date
        )
        self._table_insert("transactions", self._transaction_to_list(transaction))


    def get_all_employees(self) -> list[Employee]:
        '''
        Gets a list of all Employee objects in the database

        Returns:
            list[Employee]: A list of all employees
        '''
        return [self._list_to_employee(employee) for employee in self._table_getall('employees')]

    def get_all_items(self) -> list[InventoryItem]:
        '''
        Gets a list of all InventoryItem objecst in the database

        Returns:
            list[InventoryItem]: A list of all inventory items
        '''
        return [self._list_to_item(item) for item in self._table_getall('inventory')]

    def get_all_transactions(self) -> list[Transacion]:
        '''
        Gets a list of all Transacion objects in the database

        Returns:
            list[Transacion]: A list of all transactions
        '''
        return [self._list_to_transaction(transaction) for transaction in self._table_getall('transactions')]

    def get_all_accounts(self) -> list[FinanceAccount]:
        '''
        Gets a list of all FinanceAccount objects in the database

        Returns:
            list[FinanceAccount]: A list of all accounts
        '''
        return [self._list_to_account(transaction) for account in self._table_getall('accounts')]

    def get_employee_by_id(self, index: int) -> Employee|None:
        '''
        Retrieve an Employee by index from the database.
        Returns None if no such employee exists.

        Parameters:
            index (int): The index of the employee
        Returns:
            Employee|None: The employee or None if employee of given index does not exist
        '''
        response = self._table_get("employees", "id", f"{index}")
        if not response:
            return None
        return self._list_to_employee(response)


    def get_account_by_id(self, index: int) -> FinanceAccount|None:
        '''
        Retrieve a FinanceAccount by index from the database.
        Returns None if no such account exists.

        Parameters:
            index (int): The index of the account
        Returns:
            FinanceAccount|None: The account or None if account of given index does not exist
        '''
        response = self._table_get("accounts", "id", f"{index}")
        if not response:
            return None
        return self._list_to_account(response)

    def get_item_by_id(self, index: int) -> InventoryItem|None:
        '''
        Retrieve an InventoryItem by index from the database.
        Returns None if no such item exists.

        Parameters:
            index (int): The index of the item
        Returns:
            InventoryItem|None: The item or None if item of given index does not exist
        '''
        response = self._table_get("inventory", "id", f"{index}")
        if not response:
            return None
        return self._list_to_item(response)

    def get_transaction_by_id(self, index: int) -> Transaction|None:
        '''
        Retrieve a Transaction by index from the database.
        Returns None if no such transaction exists.

        Parameters:
            index (int): The index of the transaction
        Returns:
            Transaction|None: The transaction or None if transaction of given index does not exist
        '''
        response = self._table_get("transactions", "id", f"{index}")
        if not response:
            return None
        return self._list_to_transaction(response)

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

    def _init_tables(self) -> None:
        '''
        Initialize empty sqlite tables if none exist

        Returns:
            None
        '''

        table_defs = {
            "transactions": ["id", "account_id", "category", "item_id", "quantity", "description", "amount", "year", "month", "day"],
            "accounts": ["id", "name", "category", "currency", "balance"],
            "inventory": ["id", "name", "category", "quantity", "currency", "unit_value"],
            "employees": ["id", "username", "name", "email", "position", "salt", "password_hash", "permissions", "year", "month", "day", "auth", "expires"]
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
            table_name (str): The table to insert into
            values (list): A list of values that correspond to the table's columns
        Returns:
            None
        '''

        self._cur.execute(
            f"INSERT INTO {table_name} VALUES({', '.join([str(i) for i in values])})"
        )
        self._con.commit()

    def _table_update(self, table_name: str, key: str, value: str, **kwargs) -> None:
        '''
        Updates the values in a table where the key and value pair match.

        Parameters:
            table_name (str): The name of the table to update the row in
            key (str): The search key to determine which row to upadte
            value (str): The search value corresponding to the key
            **kwargs: Key-value pairs to determine what values to update
        '''
        kvpairs = ""
        for key in kwargs:
            kvpairs += f" {key}={kwargs[key]},"
        self._cur.execute(
            f"UPDATE {table_name} SET{kvpairs[:-1]} WHERE {key}={value}"
        )
        self._con.commit()


    def _table_get(self, table_name: str, key: str, value: str) -> list:
        '''
        Gets a single row from a table where the key and value pair match.

        Parameters:
            table_name (str): The table to search
            key (str): The column name to search by
            value (str): The value to compare
        Returns:
            list: list of all returned columns, empty if none found
        '''
        res = self._cur.execute(f"SELECT * FROM {table_name} WHERE {key}={value}")
        return res.fetchone()

    def _table_getall(self, table_name: str):
        '''
        Gets a list of all rows in a table.

        Parameters:
            table_name (str): The name of the table
        Returns:
            list: a 2D list of all of the table's rows
        '''
        res = self._cur.execute(f"SELECT * FROM {table_name}")
        return res.fetchall()


    def _list_to_employee(self, response_list: list) -> Employee:
        '''
        Converts a raw database list into an Employee object.

        Parameters:
            response_list (list): The list of raw data from the database response
        Returns:
            Employee: The converted employee object
        '''
        return Employee(
            index = response_list[0],
            username = response_list[1],
            name = response_list[2],
            email = response_list[3],
            position = response_list[4],
            salt = response_list[5],
            password_hash = response_list[6],
            permissions = Permissions(
                create_transactions = bool(response_list[7] & 1),
                delete_transactions = bool(response_list[7] & (1<<1)),
                create_inventory = bool(response_list[7] & (1<<2)),
                delete_inventory = bool(response_list[7] & (1<<3)),
                manage_employees = bool(response_list[7] & (1<<4))
            ),
            start_date = date.Date(response_list[8], response_list[9], response_list[10]),
            auth = response_list[11],
            expires = response_list[12]
        )

    def _employee_to_list(self, employee: Employee) -> list:
        '''
        Converts an Employee object into a list of raw data for the database.

        Parameters:
            employee (Employee): The employee to convert
        Returns:
            list: The list of raw values
        '''
        return [employee.index, f"'{employee.username}'", f"'{employee.name}'",
                f"'{employee.email}'", f"'{employee.position}'", f"{employee.salt}",
                f"'{employee.password_hash}'", 
                (employee.permissions.create_transactions << 0) | \
                (employee.permissions.delete_transactions << 1) | \
                (employee.permissions.create_inventory << 2) | \
                (employee.permissions.delete_inventory << 3) | \
                (employee.permissions.manage_employees << 4),
                employee.start_date.year,
                employee.start_date.month,
                employee.start_date.day,
                f"'{employee.auth}'",
                employee.expires
                ]

    def _list_to_transaction(self, response_list: list) -> Transaction:
        '''
        Converts a raw database list to a Transaction object.

        Parameters:
            response_list (list): The list of raw data from the database response
        Returns:
            Transaction: The converted transaction object
        '''
        account = self.get_account_by_id(response_list[1])
        return Transaction(
            index = response_list[0],
            account = account,
            category = response_list[2],
            item = self.get_item_by_id(response_list[3]),
            quantity = response_list[4],
            description = response_list[5],
            amount = money.Money(response_list[6], account.currency),
            date = date.Date(response_list[7], response_list[8], response_list[9])
        )

    def _transaction_to_list(self, transaction: Transaction) -> list:
        '''
        Converts a Transaction object into a list of raw data for the database.

        Parameters:
            transaction (Transaction): The transaction to convert
        Returns:
            list: The list of raw values
        '''
        return [transaction.index, transaction.account.index, f"'{transaction.category}'", 
                transaction.item.index,
                transaction.quantity, f"'{transaction.description}'", 
                transaction.amount.get_value_cents(), transaction.date.year, 
                transaction.date.month, transaction.date.day]


    def _account_to_list(self, account: FinanceAccount) -> list:
        '''
        Converts a FinanceAccount object into a list of raw data for the database.

        Parameters:
            account (FinanceAccount): The transaction to convert
        Returns:
            list: The list of raw values
        '''
        return [account.index, f"'{account.name}'", 
                f"'{account.category}'"
                f"'{account.currency}'", 
                account.balance.get_value_cents()]

    def _item_to_list(self, item: InventoryItem) -> list:
        '''
        Converts an InventoryItem object into a list of raw data for the database.

        Parameters:
            item (InventoryItem): The item to convert
        Returns:
            list: The list of raw values
        '''
        return [
            item.index,
            f"'{item.name}'",
            f"'{item.category}'",
            item.quantity,
            f"'{item.unit_value.get_currency()}'",
            item.unit_value.get_value_cents()
        ]

    def _list_to_account(self, response_list: list) -> FinanceAccount:
        '''
        Converts a raw database list to a FinanceAccount object.

        Parameters:
            response_list (list): The list of raw data from the database response
        Returns:
            FinanceAccount: The converted account object
        '''
        return FinanceAccount(
            index = response_list[0],
            name = response_list[1],
            category = response_list[2],
            currency = response_list[3],
            balance = money.Money(response_list[4], response_list[3])
        )

    def _list_to_item(self, response_list: list) -> InventoryItem:
        '''
        Converts a raw database list to a FinanceAccount object.

        Parameters:
            response_list (list): The list of raw data from the database response
        Returns:
            FinanceAccount: The converted account object
        '''
        return InventoryItem(
            index = response_list[0],
            name = response_list[1],
            category = response_list[2],
            quantity = response_list[3],
            unit_value = money.Money(response_list[5],response_list[4])
        )

