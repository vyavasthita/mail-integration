# import important module
from datetime import datetime
from dateutil import parser


def find_datetime_from_strftime(str_datetime):
    return parser.parse(str_datetime)


def change_format_from_datetime(dt: datetime, new_format: str):
    return dt.strftime("%Y-%m-%d")
