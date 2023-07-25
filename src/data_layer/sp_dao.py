from mysql.connector import Error, Warning
from src.data_layer.db_connection import DBConnection
from src.utils.api_logger import ApiLogger


class SPDao:
    @staticmethod
    def call_sp(name: str):
        ApiLogger.log_info("calling stored procedure to create full text index.")

        with DBConnection() as db_connection:
            try:
                db_connection.cursor.callproc(name)
            except Warning as warning:
                ApiLogger.log_info(warning)
            except Error as error:
                ApiLogger.log_info(error.msg)
