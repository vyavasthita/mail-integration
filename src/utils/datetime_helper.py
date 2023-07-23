"""Helper module to perform date time related operations.

@file datetime_helper.py
@author Dilip Kumar Sharma
@date 19 July 2023

About; -
--------
    Helper module to perform date time related operations.
    This is used by rule engine to create query based on time.
    Eg. Converting datetime object to string, subtracting days from given date.
"""

# Core python packages
from datetime import datetime, date, timedelta
from dateutil import parser


def find_datetime_from_strftime(str_datetime: str) -> datetime:
    """To find out the time format from email metadata.

    Args:
        str_datetime (str): Given time format

    Returns:
        datetime: datetime object representing the format of datetime
    """
    return parser.parse(str_datetime)


def change_format_from_datetime(dt: datetime, date_format: str) -> str:
    """To Change format

    Args:
        dt (datetime): Given datetime
        date_format (str): Target datetime format

    Returns:
        str: Datetime in string format
    """
    return dt.strftime(date_format)


def get_today() -> None:
    """Get today date

    Returns:
        None:
    """
    return date.today()


def subtract_days(source_date: date, no_of_days: int) -> date:
    """Subtract no of days from a given date

    Args:
        source_date (date): Days to be subtracted from
        no_of_days (int): Days to be subtracted

    Returns:
        date: date post subtraction
    """
    return source_date - timedelta(days=no_of_days)


def add_days(source_date: date, no_of_days: int) -> date:
    """Add no of days in a given date

    Args:
        source_date (date): Days to be added from
        no_of_days (int): Days to be added

    Returns:
        date: date post addition
    """
    return source_date + timedelta(days=no_of_days)
