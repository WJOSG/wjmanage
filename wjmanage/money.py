class Money:
    '''
    '''

    def __init__(self, value_cents: int, currency: str):
        '''
        '''

        self._value = value_cents
        self._currency = currency

    def __repr__(self):
        '''
        '''

        return f"{self._value // 100}.{(self.value % 100):02} ({self._currency})"

    def __add__(self, other: Money):
        '''
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value + other._value, self.currency)

    def __sub__(self, other: Money):
        '''
        '''

        if self._currency != other._currency:
            raise TypeError(f"Incompatible currencies: '{self._currency}' and '{other._currency}'")

        return Money(self._value - other._value, self.currency)

    def __mul__(self, other: int):
        '''
        '''

        return Money(self._value * other, self.currency)

    def __div__(self, other: int):
        '''
        '''

        return Money(self._value // other, self.currency)
