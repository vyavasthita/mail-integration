from mysql.connector import Error, errorcode, Warning
from src.db_init import DBConnection
from utils.api_logger import ApiLogger


class EmailFetchDao:
    @staticmethod
    def add_emails(db_data: dict):
        add_label = """
            INSERT INTO label(label_id, name) value(%s, %s) ON DUPLICATE KEY UPDATE name = name
        """

        add_email = """
            INSERT INTO email(message_id, is_read) value(%s, %s) ON DUPLICATE KEY UPDATE is_read = is_read
        """

        add_email_label = """
            INSERT INTO email_label(label_id, message_id) value(%s, %s)
        """

        add_sender = """
            INSERT INTO email_sender(message_id, sender) value(%s, %s) ON DUPLICATE KEY UPDATE sender = sender
        """

        add_receiver = """
            INSERT INTO email_receiver(message_id, receiver) value(%s, %s) ON DUPLICATE KEY UPDATE receiver = receiver
        """

        add_subject = """
            INSERT INTO email_subject(message_id, subject) value(%s, %s) ON DUPLICATE KEY UPDATE subject = subject
        """

        add_content = """
            INSERT INTO email_content(message_id, content) value(%s, %s) ON DUPLICATE KEY UPDATE content = content
        """

        add_date = """
            INSERT INTO email_date(message_id, received) value(%s, %s) ON DUPLICATE KEY UPDATE received = received
        """

        with DBConnection() as db_connection:
            db_connection.connection.start_transaction()

            db_connection.cursor.executemany(add_label, db_data["label"])
            db_connection.cursor.executemany(add_email, db_data["email"])
            db_connection.cursor.executemany(add_email_label, db_data["email_label"])
            db_connection.cursor.executemany(add_sender, db_data["sender"])
            db_connection.cursor.executemany(add_receiver, db_data["receiver"])
            db_connection.cursor.executemany(add_subject, db_data["subject"])
            # db_connection.cursor.executemany(add_content, db_data["content"])
            db_connection.cursor.executemany(add_date, db_data["date"])

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
                ApiLogger.log_info(error.errno, error.msg)
