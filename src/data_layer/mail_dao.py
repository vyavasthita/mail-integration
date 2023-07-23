"""Dao for connecting to database for writing mail data.

@file mail_dao.py
@author Dilip Kumar Sharma
@date 20th July 2023

About; -
--------
    This module lets other modules talks to database.
    This helps us providing loose coupling between python packages and database
"""
# Core python packages
from typing import List

# Application packages
from src.data_layer.db_connection import DBConnection
from src.mail_engine.mail_data import MailData
from src.utils.api_logger import ApiLogger


class MailDao:
    @staticmethod
    def create(mails_data: List[MailData]) -> None:
        """
        Create record in database.

        Args:
            mails_data (List[MailData]): Data to be inserted into database.
        """
        ApiLogger.log_info("Writing email data to database using sql transaction.")
        with DBConnection() as db_connection:
            db_connection.connection.start_transaction()

            for mail_data in mails_data:
                db_connection.cursor.executemany(
                    mail_data.query_string, mail_data.query_data
                )

            db_connection.connection.commit()  # commit changes

    @staticmethod
    def read(query: str) -> None:
        """
        Reading data from database

        Args:
            query (str): query to be executed to fetch records
        """
        with DBConnection() as db_connection:
            db_connection.cursor.execute(query)
            return db_connection.cursor.fetchall()
