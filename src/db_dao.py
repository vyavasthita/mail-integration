from src.db_init import DBConnection


class EmailFetchDao:
    @staticmethod
    def add_emails(db_data: dict):
        add_label = """
            INSERT INTO label(label_id, name) value(%s, %s) ON DUPLICATE KEY UPDATE name = name
            """

        add_receiver = """
            INSERT INTO receiver(email) value(%s) ON DUPLICATE KEY UPDATE email = email
            """

        add_message = """
            INSERT INTO email_message(message_id, message, receiver) value(%s, %s, %s) ON DUPLICATE KEY UPDATE message = message, receiver = receiver
            """

        add_sender = """
            INSERT INTO sender(email, message) value(%s, %s) ON DUPLICATE KEY UPDATE email = email, message = message
            """

        add_subject = """
            INSERT INTO subject(value, message) value(%s, %s) ON DUPLICATE KEY UPDATE value = value, message = message
            """

        add_date_info = """
            INSERT INTO date_info(mail_date, message) value(%s, %s) ON DUPLICATE KEY UPDATE mail_date = mail_date, message = message
            """

        with DBConnection() as db_connection:
            db_connection.connection.start_transaction()

            db_connection.cursor.executemany(add_label, db_data["label"])
            db_connection.cursor.executemany(add_receiver, db_data["receiver"])
            # db_connection.cursor.executemany(add_message, db_data["message"])
            # db_connection.cursor.executemany(add_sender, db_data["sender"])
            # db_connection.cursor.executemany(add_subject, db_data["subject"])
            # db_connection.cursor.executemany(add_date_info, db_data["date_info"])

            db_connection.connection.commit()  # commit changes
