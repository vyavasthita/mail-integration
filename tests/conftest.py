import pytest
from datetime import date, timedelta
from mysql.connector import connect
from src import env_configuration
from src.initialize import create_ftsi


@pytest.fixture
def db_connection():
    try:
        connection = connect(
            host=env_configuration.MYSQL_HOST,
            user=env_configuration.MYSQL_USER,
            database=env_configuration.MYSQL_DB,
            password=env_configuration.MYSQL_PASSWORD,
        )
        yield connection
    except Exception:
        pass
    finally:
        # truncate date post verification
        connection.cursor().execute("SET foreign_key_checks = 0")
        connection.cursor().execute("TRUNCATE TABLE label")
        connection.cursor().execute("TRUNCATE TABLE email_sender")
        connection.cursor().execute("TRUNCATE TABLE email_receiver")
        connection.cursor().execute("TRUNCATE TABLE email_subject")
        connection.cursor().execute("TRUNCATE TABLE email_content")
        connection.cursor().execute("TRUNCATE TABLE email_date")
        connection.cursor().execute("TRUNCATE TABLE email")
        connection.cursor().execute("SET foreign_key_checks = 1")
        connection.commit()
        connection.close()


# def clean_up_tables():
#     # truncate date post verification
#     connection.cursor().execute("SET foreign_key_checks = 0")
#     connection.cursor().execute("TRUNCATE TABLE email_sender")
#     connection.cursor().execute("TRUNCATE TABLE email_receiver")
#     connection.cursor().execute("TRUNCATE TABLE email_subject")
#     connection.cursor().execute("TRUNCATE TABLE email_content")
#     connection.cursor().execute("TRUNCATE TABLE email_date")
#     connection.cursor().execute("TRUNCATE TABLE email")
#     connection.cursor().execute("SET foreign_key_checks = 1")
#     connection.commit()


@pytest.fixture
def set_up_test_data_1(db_connection):
    add_email = """
        INSERT INTO email(message_id, is_read) value(%s, %s) ON DUPLICATE KEY UPDATE is_read = is_read
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

    email_data = [
        ("message_id_1", True),
        ("message_id_2", False),
        ("message_id_3", True),
        ("message_id_4", False),
    ]

    sender_data = [
        ("message_id_1", "someemail@gmail.com"),
        ("message_id_2", "anotheremail@gmail.com"),
        ("message_id_3", "dilipsharma@gmail.com"),
        ("message_id_4", "somecompany@gmail.com"),
    ]

    receiver_data = [
        ("message_id_1", "dilip@gmail.com"),
        ("message_id_2", "user@gmail.com"),
        ("message_id_3", "someuser@gmail.com"),
        ("message_id_4", "testuser@gmail.com"),
    ]

    subject_data = [
        ("message_id_1", "You inteview has been scheduled"),
        ("message_id_2", "Meeting has been cancelled"),
        ("message_id_3", "Nothing is cancelled"),
        ("message_id_4", "is it cancelled"),
    ]

    content_data = [
        ("message_id_1", "You inteview has been scheduled"),
        ("message_id_2", "Meeting has been cancelled"),
        ("message_id_3", "Nothing is cancelled"),
        ("message_id_4", "is it cancelled"),
    ]

    date_data = [
        ("message_id_1", "2023-07-23"),
        ("message_id_2", "2023-07-21"),
        ("message_id_3", "2023-07-18"),
        ("message_id_4", "2023-07-20"),
    ]

    db_connection.start_transaction()

    db_connection.cursor().executemany(add_email, email_data)
    db_connection.cursor().executemany(add_sender, sender_data)
    db_connection.cursor().executemany(add_receiver, receiver_data)
    db_connection.cursor().executemany(add_subject, subject_data)
    db_connection.cursor().executemany(add_content, content_data)
    db_connection.cursor().executemany(add_date, date_data)

    db_connection.commit()

    create_ftsi()


@pytest.fixture
def today_date():
    return date.today()
