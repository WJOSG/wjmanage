class Date:
    '''
    '''

    def __init__(self, year: int, month: int, day: int):
        '''
        '''

        if month not in range(1, 13):
            raise ValueError(f"Invalid month: {month}")

        if day not in range(1, 32):
            raise ValueError(f"Invalid day: {day}")

        self.year = year
        self.month = month
        self.day = day

    def __repr__(self):
        '''
        '''

        return f"{self.year:04}.{self.month:02}.{self.day:02}"
