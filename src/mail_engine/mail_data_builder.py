"""Validates database connection.

@file mail_data_builder.py
@author Dilip Kumar Sharma
@date 20th July 2023

About; -
--------
    Validates whether or not we are connected to database
"""
# Core python packages
from dataclasses import dataclass, field

# Application packages
from src.mail_engine.mail_data import MailData
from src.data_layer.mail_dao import MailDao


@dataclass
class MailDataBuilder:
    mail_data: list[MailData] = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def construct_write_data(self):
        add_label = """
            INSERT INTO label(label_id, name) value(%s, %s) ON DUPLICATE KEY UPDATE name = name
        """

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

        self.mail_data.append(MailData(add_label, self.data["label"]))
        self.mail_data.append(MailData(add_email, self.data["email"]))
        self.mail_data.append(MailData(add_sender, self.data["sender"]))
        self.mail_data.append(MailData(add_receiver, self.data["receiver"]))
        self.mail_data.append(MailData(add_subject, self.data["subject"]))
        self.mail_data.append(MailData(add_date, self.data["date"]))
        self.mail_data.append(MailData(add_content, self.data["content"]))

    def write_to_db(self) -> None:
        """
        Triggers writing data to db
        """
        MailDao.create(self.mail_data)
