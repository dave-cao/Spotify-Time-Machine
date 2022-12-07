from datetime import datetime, timedelta
from random import randrange


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_random_date():
    """Returns a random date string from 1958 to today!"""
    start_date = datetime.strptime("1958-08-04", "%Y-%m-%d")
    end_date = datetime.now()

    date = random_date(start_date, end_date)

    string_date = datetime.strftime(date, "%Y-%m-%d")
    return string_date
