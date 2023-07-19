import os
import ast
from dotenv import load_dotenv


# The root directory
base_dir = os.path.abspath(os.path.dirname(__name__))

env_by_name = dict(development=".env.dev", automated_testing=".env.aut_test")

environment = os.getenv("BUILD_ENV")

if environment is None:
    print(
        f"'BUILD_ENV' environment variable is not set. Please set it among environments {env_by_name.keys()}"
    )

if environment not in env_by_name.keys():
    print(f"Invalid {environment}. Available Environments {env_by_name.keys()}")

print("Using 'development' environment.")

environment = "development"

for environment_file in env_by_name.values():
    load_dotenv(
        dotenv_path=os.path.join(base_dir, environment_file)
    )  # to load .env file. .flaskenv file is automatically loaded without using load_dotenv()


class DevelopmentConfig:
    # Flaks CLI configurations
    CLIENT_ID = os.getenv("CLIENT_ID_DEV")
    PROJECT_ID = os.getenv("PROJECT_ID_DEV")
    AUTH_URI = os.getenv("AUTH_URI_DEV")
    TOKEN_URI = os.getenv("TOKEN_URI_DEV")
    AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL_DEV")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET_DEV")
    REDIRECT_URIS = os.getenv("REDIRECT_URIS_DEV")

    SCOPES_DEV = os.getenv("SCOPES_DEV")
    SCOPES = SCOPES_DEV.split(", ")

    USER_ID = os.getenv("USER_ID_DEV")

    MYSQL_HOST = os.getenv("MYSQL_HOST_DEV")
    MYSQL_USER = os.getenv("MYSQL_USER_DEV")
    MYSQL_DB = os.getenv("MYSQL_DB_DEV")
    USER_ID = os.getenv("USER_ID_DEV")
    MYSQL_PORT = os.getenv("MYSQL_PORT_DEV")

    # Configuration file for logging
    LOG_CONFIG_FILE = "./config/development/logging.conf"

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv("LOGS_DIR_DEV") or "/tmp/mail_api_logs"

    # Log File name
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME_DEV") or "mail_api.log"


class AutomatedTestingConfig:
    pass


config_by_name = dict(
    development=DevelopmentConfig(), automated_testing=AutomatedTestingConfig()
)
