"""Environment variable configuration.

@file env_config.py
@author Dilip Kumar Sharma
@date 20 July 2023

About; -
--------
    To read application configuration from .env.* file.
"""

# Core python packages
import os
import sys

# Third party packages
from dotenv import load_dotenv


build_environment = os.getenv("BUILD_ENV")  # development, qa or production
run_environment = os.getenv("RUN_ENV") or "app"  # application or unit tests

# The root directory
base_dir = os.path.abspath(os.path.dirname(__name__))
build_environment_base_path = os.path.join(base_dir, "configuration", build_environment)


env_by_name = dict(
    app=os.path.join(build_environment_base_path, ".env.app"),
    test=os.path.join(build_environment_base_path, ".env.test"),
)

if run_environment not in env_by_name.keys():
    print(f"Invalid {run_environment}. Available Environments {env_by_name.keys()}")
    sys.exit(0)


for environment_file in env_by_name.values():
    load_dotenv(dotenv_path=environment_file)


class AppConfig:
    CLIENT_ID = os.getenv("CLIENT_ID_APP")
    PROJECT_ID = os.getenv("PROJECT_ID_APP")
    AUTH_URI = os.getenv("AUTH_URI_APP")
    TOKEN_URI = os.getenv("TOKEN_URI_APP")
    AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL_APP")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET_APP")
    REDIRECT_URIS = os.getenv("REDIRECT_URIS_APP")
    API_URL = os.getenv("API_URL_APP")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN_APP") or None

    USER_ID = os.getenv("USER_ID_APP")

    MYSQL_HOST = os.getenv("MYSQL_HOST_APP")
    MYSQL_USER = os.getenv("MYSQL_USER_APP")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD_APP")
    MYSQL_DB = os.getenv("MYSQL_DB_APP")
    USER_ID = os.getenv("USER_ID_APP")
    MYSQL_PORT = os.getenv("MYSQL_PORT_APP")

    # Configuration file for logging
    LOG_CONFIG_FILE = f"./configuration/{build_environment}/logging.conf"

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv("LOGS_DIR_APP") or "/tmp/mail_api_logs"

    # Log File name
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME_APP") or "mail_api.log"


class TestConfig:
    CLIENT_ID = os.getenv("CLIENT_ID_TEST")
    PROJECT_ID = os.getenv("PROJECT_ID_TEST")
    AUTH_URI = os.getenv("AUTH_URI_TEST")
    TOKEN_URI = os.getenv("TOKEN_URI_TEST")
    AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL_TEST")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET_TEST")
    REDIRECT_URIS = os.getenv("REDIRECT_URIS_TEST")
    API_URL = os.getenv("API_URL_TEST")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN_TEST") or None

    USER_ID = os.getenv("USER_ID_TEST")

    MYSQL_HOST = os.getenv("MYSQL_HOST_TEST")
    MYSQL_USER = os.getenv("MYSQL_USER_TEST")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD_TEST")
    MYSQL_DB = os.getenv("MYSQL_DB_TEST")
    USER_ID = os.getenv("USER_ID_TEST")
    MYSQL_PORT = os.getenv("MYSQL_PORT_TEST")

    # Configuration file for logging
    LOG_CONFIG_FILE = f"./configuration/{build_environment}/logging.conf"

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv("LOGS_DIR_TEST") or "/tmp/mail_api_logs"

    # Log File name
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME_TEST") or "mail_api.log"


config_by_name = dict(app=AppConfig(), test=TestConfig())
