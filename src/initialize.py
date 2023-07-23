"""To Initialize application.

@file initialize.py
@author Dilip Kumar Sharma
@date 19 July 2023

About; -
--------
    It is responsible for initializing app.
"""

# Core python packages
from functools import wraps

# Application packages
from src import env_configuration, app_configuration
from src.utils.gen_credential_data import gen_data
from src.utils.file_helper import write_to_json
from src.utils.api_logger import ApiLogger
from src.data_layer.sp_dao import SPDao
from src.auth.auth import Auth


def init_credential_json() -> None:
    """
    Read gmail credentials from .env file and write them to a json file because
    gmail api uses .json file to read credentials.
    """
    ApiLogger.log_debug("Creating credential json file.")

    write_to_json(
        json_string=gen_data(env_configuration=env_configuration),
        out_file_path="credentials.json",
    )


def create_ftsi() -> None:
    """
    Create Full text search indexes by calling stored procedure.
    Full text search indexes are created post inserting data into tables to improve performance.
    """
    SPDao.call_sp(app_configuration.api_config.index_sp_name)


def check_ftsi(func):
    """
    Decorator to create stored procedure before proceeding further.

    Args:
        func: Function to be decorated

    Returns:
        func: decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        create_ftsi()
        return func(*args, **kwargs)

    return wrapper


def auth() -> None:
    """
    Trigger Authorization flow.
    This creates a token.json file.
    """
    auth = Auth()
    auth.start()


def un_auth() -> None:
    """
    Triggers un authorization flow.
    Delete token.json file.
    This is marked as un authorization.
    Next time we run the app to trigger authorization, auth flow will run again
    and token.json file will be created.
    """
    auth = Auth()
    auth.un_authenticate()


def validate_auth(func):
    """
    Decorator to trigger auth flow.

    Args:
        func: Function to be decorated

    Returns:
        func: decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth()
        return func(*args, **kwargs)

    return wrapper
