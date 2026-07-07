class Date:
    '''
    A simple class for storing a date in the database

    Parameters:
        year (int): The year
        month (int): The month in the range [1,12]
        day (int): The day in the range [1,31]
    '''

    def __init__(self, year: int, month: int, day: int) -> None:
        '''
        Initialize a Date object. Raises a ValueError for improper date.

        Parameters:
            year (int): The year
            month (int): The month, must be in the range [1,12]
            day (int): The day, must be in the range [1,31]

        Returns:
            None
        '''

        if month not in range(1, 13):
            raise ValueError(f"Invalid month: {month}")

        if day not in range(1, 32):
            raise ValueError(f"Invalid day: {day}")

        self.year = year
        self.month = month
        self.day = day

    def __repr__(self) -> str:
        '''
        Represents the date as a string in the format:
        "YYYY.MM.DD"

        Returns:
            str: The date encoded in "YYYY.MM.DD"
        '''

        return f"{self.year:04}.{self.month:02}.{self.day:02}"
