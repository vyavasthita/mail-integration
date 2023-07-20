# import important module
from datetime import datetime, date, timedelta
from dateutil import parser


def find_datetime_from_strftime(str_datetime):
    return parser.parse(str_datetime)


def change_format_from_datetime(dt: datetime, date_format: str):
    return dt.strftime(date_format)


def get_today():
    return date.today()


def subtract_days(source_date: date, no_of_days: int):
    return source_date - timedelta(days=no_of_days)


def add_days(source_date: date, no_of_days: int):
    return source_date + timedelta(days=no_of_days)
