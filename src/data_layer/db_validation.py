"""Validates database connection.

@file db_validation.py
@author Dilip Kumar Sharma
@date 20th July 2023

About; -
--------
    Validates whether or not we are connected to database
"""
# Core python packages
from functools import wraps

# Application packages
from src.data_layer.db_connection import DBConnection
from src.utils.api_logger import ApiLogger


def check_db_connection(func):
    """
    Decorator to validate db connection

    Args:
        func: Function to be decorated

    Returns:
        func: decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ApiLogger.log_info(
            f"Checking if we are connected to database. Request coming from {func.__name__}."
        )

        with DBConnection() as db_connection:
            if db_connection.connection.is_connected():
                ApiLogger.log_info("Congratulations!. Db connection is successful.")

        return func(*args, **kwargs)

    return wrapper
