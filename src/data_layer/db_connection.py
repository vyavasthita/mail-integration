"""To connect to database.

@file db_cpnnection.py
@author Dilip Kumar Sharma
@date 19th July 2023

About; -
--------
    It connects with mysql database using python mysql connector
"""

# Core python packages
import sys

# Third party packages
from mysql.connector import connect, Error, errorcode

# Application packages
from src import env_configuration
from src.utils.api_logger import ApiLogger


class DBConnection:
    config = {
        "host": env_configuration.MYSQL_HOST,
        "database": env_configuration.MYSQL_DB,
        "user": env_configuration.MYSQL_USER,
        "password": env_configuration.MYSQL_PASSWORD,
        "raise_on_warnings": True,
        "autocommit": True,
    }

    def __init__(self) -> None:
        try:
            self.connection = connect(**DBConnection.config)
            self.cursor = self.connection.cursor()
            ApiLogger.log_info(
                f"User '{self.connection.user}' is connected to '{self.connection.database}' database."
            )
        except Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                ApiLogger.log_critical(
                    "Something is wrong with your user name or password"
                )
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                ApiLogger.log_critical("Database does not exist")
            else:
                ApiLogger.log_critical(str(error))

            ApiLogger.log_critical("We are not connected to databse. Exiting...")
            sys.exit(0)
        except Exception as error:
            ApiLogger.log_critical(
                f"Failed to connect to database. {str(error)} Exiting..."
            )
            sys.exit(0)

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ApiLogger.log_info("Disconnecting from database.")
        if self.connection.is_connected():
            self.cursor.close()
            # close db connection
            self.connection.close()
            ApiLogger.log_info("Disconneced from database.")
