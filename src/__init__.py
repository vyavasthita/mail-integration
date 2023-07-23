"""Setting the configurations.

@file __init__.py
@author Dilip Kumar Sharma
@date 19 July 2023

About; -
--------
    All other python modules uses this file to get configuration objects.
    This is used across application for both app run and running unit tests.
"""
# Core python packages
import os

# Application packages
from src.config.env_config import config_by_name
from src.config.app_config import AppConfigParser


environment = os.getenv("BUILD_ENV")  # development or qa or production
run_environment = os.getenv("RUN_ENV") or "app"  # running application or unit tests


def create_log_directory() -> None:
    """
    Create log directory
    """

    base_dir = os.path.abspath(os.path.dirname(__name__))

    if not os.path.exists(os.path.join(base_dir, env_configuration.LOGS_DIR)):
        os.mkdir(os.path.join(base_dir, env_configuration.LOGS_DIR))


app_config_file_path = os.path.join(
    os.getcwd(), "configuration", environment, "app_config.json"
)

# get environment for app run or running unit tests
env_configuration = config_by_name[run_environment]

app_config_parser = AppConfigParser(file_path=app_config_file_path)

app_configuration = app_config_parser.parse()
