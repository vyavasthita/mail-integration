from typing import List
from src.data_layer.db_connection import DBConnection
from src.mail_engine.mail_data import MailData
from src.utils.api_logger import ApiLogger


class MailDao:
    @staticmethod
    def create(mails_data: List[MailData]):
        ApiLogger.log_info("Writing email data to database.")
        with DBConnection() as db_connection:
            db_connection.connection.start_transaction()

            for mail_data in mails_data:
                db_connection.cursor.executemany(
                    mail_data.query_string, mail_data.query_data
                )

            db_connection.connection.commit()  # commit changes

    @staticmethod
    def read(query):
        with DBConnection() as db_connection:
            db_connection.cursor.execute(query)
            return db_connection.cursor.fetchall()
