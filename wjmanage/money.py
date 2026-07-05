class Money:
    '''
    A class representing an amount of money (positive or negative)
    for a given currency, using fixed point (2 decimal places).
    '''

    def __init__(self, value_cents: int, currency: str) -> None:
        '''
        Initialize a Money object.

        Parameters:
            value_cents: int - The amount of money in cents (eg. $12.34 -> 1234 cents)
            currency: str - A string representing the type of currency (USD, GBP, PLN, ...)

        Returns:
            None

        '''

        self._value = value_cents
        self._currency = currency

    def get_value(self) -> int:
        '''
        '''
        return self._value

    def get_currency(self) -> str:
        '''
        '''
        return self._currency

    def set_value(self, value_cents: int) -> None:
        '''
        '''
        self._value = value_cents

    def set_currency(self, currency: str) -> None:
        '''
        '''
        self._currency = currency

    def __repr__(self) -> str:
        '''
        '''

        return f"{self._value // 100}.{(self.value % 100):02} ({self._currency})"

    def __add__(self, other: Money) -> Money:
        '''
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value + other._value, self.currency)

    def __sub__(self, other: Money) -> Money:
        '''
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value - other._value, self.currency)

    def __mul__(self, other: int) -> Money:
        '''
        '''

        return Money(self._value * other, self.currency)

    def __floordiv__(self, other: int) -> Money:
        '''
        '''

        return Money(self._value // other, self.currency)
