class Money:
    '''
    A class representing an amount of money (positive or negative)
    for a given currency, using fixed point (2 decimal places).
    '''

    def __init__(self, value_cents: int, currency: str) -> None:
        '''
        Initialize a Money object. Raises a TypeError if the value is not an `int`
        or a subclass of `int`. The currency is automatically capitalized.

        Parameters:
            value_cents (int): The amount of money in cents (eg. $12.34 -> 1234 cents)
            currency (str): A string representing the type of currency (USD, GBP, PLN, ...)

        Returns:
            None
        '''

        if not isinstance(value_cents, int):
            raise TypeError(f"The value: {value_cents} is not an integer.")
        self._value = value_cents
        self._currency = currency.upper()

    def get_value_cents(self) -> int:
        '''
        Get the value of money in cents

        Returns:
            int: The value in cents
        '''
        return self._value

    def get_currency(self) -> str:
        '''
        Get the money's currency

        Returns:
            str: The currency
        '''
        return self._currency

    def set_value(self, value_cents: int) -> None:
        '''
        Set the value of money in cents.
        Raises a TypeError if the value is not an `int` or a subclass of `int`.

        Parameters:
            value_cents (int): The value of the money in cents

        Returns:
            None
        '''
        if not isinstance(value_cents, int):
            raise TypeError(f"The value: {value_cents} is not an integer.")
        self._value = value_cents

    def set_currency(self, currency: str) -> None:
        '''
        Set the money's currency.

        Parameters:
            currency (str): The currency to set, is automatically capitalized

        Returns:
            None
        '''
        self._currency = currency.upper()

    def __repr__(self) -> str:
        '''
        Represents the amount of money as a string

        Returns:
            str: String representation of the value
        '''

        return f"{self._value // 100}.{(self._value % 100):02} ({self._currency})"

    def __add__(self, other: Money) -> Money:
        '''
        Adds two values of the same currency using the '+' operator.
        Raises a TypeError for incompatible currencies

        Parameters:
            other (Money): The RHS of the '+' operator

        Returns:
            Money: The sum of the two values
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value + other._value, self._currency)

    def __sub__(self, other: Money) -> Money:
        '''
        Subtracts two values of the same currency using the '-' operator.
        Raises a TypeError for incompatible currencies

        Parameters:
            other (Money): The RHS of the '-' operator

        Returns:
            Money: The sum of the two values
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value - other._value, self._currency)

    def __mul__(self, other: int) -> Money:
        '''
        Multiplies the value of money by an integer scalar using the '*' operator.

        Parameters:
            other (int): The RHS of the '*' operator

        Returns:
            Money: The product of the two values
        '''

        return Money(self._value * other, self._currency)

    def __floordiv__(self, other: int) -> Money:
        '''
        Divides the value of money by an integer scalar using the '//' operator.
        This is an integer division internally, so is truncated by the cent.

        Parameters:
            other (int): The RHS of the '//' operator

        Returns:
            Money: The quotient of the division

        '''

        return Money(self._value // other, self._currency)


    def percent(self, percentage: int) -> Money:
        '''
        Calculates the value of an integer percentage of the money, truncated by the cent.

        Parameters:
            percentage (int): The percantage to calculate

        Returns:
            Money: The result of the percentage calculation
        '''

        return self * percentage // 100

    def __eq__(self, other: Money) -> bool:
        '''
        Compares the equality of two monetary values using the '==' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '==' operator

        Returns:
            bool: The truth of the equality
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value == other._value


    def __ne__(self, other):
        '''
        Compares the inequality two monetary values using the '!=' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '!=' operator

        Returns:
            bool: The truth of the inequality
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value != other._value

    def __gt__(self, other: Money) -> bool:
        '''
        Greater than comparison of two monetary values using the '>' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '>' operator

        Returns:
            bool: The truth of the comparison
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value > other._value

    def __lt__(self, other: Money) -> bool:
        '''
        Less than comparison of two monetary values using the '<' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '<' operator

        Returns:
            bool: The truth of the comparison
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value < other._value

    def __le__(self, other: Money) -> bool:
        '''
        Less or equal comparison of two monetary values using the '<=' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '<=' operator

        Returns:
            bool: The truth of the comparison
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value <= other._value

    def __ge__(self, other: Money) -> bool:
        '''
        Greater or equal comparison of two monetary values using the '>=' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '>=' operator

        Returns:
            bool: The truth of the comparison
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        return self._value >= other._value

    def __iadd__(self, other: Money) -> Money:
        '''
        Addition assignment for monetary value using the '+=' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '+=' operator

        Returns:
            Money: The LHS of the '-=' operator
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        self._value += other._value
        return self

    def __isub__(self, other: Money) -> Money:
        '''
        Subtraction assignment for monetary value using the '-=' operator.
        Raises a TypeError for incompatible currencies.

        Parameters:
            other (Money): The RHS of the '-=' operator

        Returns:
            Money: The LHS of the '-=' operator
        '''
        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")
        self._value -= other._value
        return self

    def __imul__(self, other: int) -> Money:
        '''
        Multiplication assignment for monetary value using the '*=' operator.
        Raises a TypeError for non-integer values.

        Parameters:
            other (int): The RHS of the '*=' operator

        Returns:
            Money: The LHS of the '*=' operator
        '''
        if not isinstance(other, int):
            raise TypeError(f"The value: {other} is not an integer.")
        self._value *= other
        return self

    def __ifloordiv__(self, other: int) -> Money:
        '''
        Division assignment for monetary value using the '//=' operator.
        Raises a TypeError for non-integer values.

        Parameters:
            other (int): The RHS of the '//=' operator

        Returns:
            Money: The LHS of the '//=' operator
        '''
        if not isinstance(other, int):
            raise TypeError(f"The value: {other} is not an integer.")
        self._value //= other
        return self


    def __neg__(self) -> Money:
        '''
        Negation of the monetary value using the unary '-' operator.
        Eg. -Money(1234, 'USD') == Money(-1234, 'USD')

        Returns:
            Money: The negated monetary value
        '''
        return Money(-self._value, self._currency)

