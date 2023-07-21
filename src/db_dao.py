from typing import List
from mysql.connector import Error, errorcode, Warning
from src.db_init import DBConnection
from src.mail_data import MailData
from utils.api_logger import ApiLogger


class MailDao:
    @staticmethod
    def create(mails_data: List[MailData]):
        with DBConnection() as db_connection:
            db_connection.connection.start_transaction()

            for mail_data in mails_data:
                db_connection.cursor.executemany(
                    mail_data.query_string, mail_data.query_data
                )

            db_connection.connection.commit()  # commit changes


class SPDao:
    @staticmethod
    def call_sp(name: str):
        with DBConnection() as db_connection:
            try:
                db_connection.cursor.callproc(name)
            except Warning as warning:
                ApiLogger.log_info(warning)
            except Error as error:
                ApiLogger.log_info(error.msg)
