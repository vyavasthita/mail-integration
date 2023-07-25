"""Read gmail data using gmail api.

@file mail_reader.py
@author Dilip Kumar Sharma
@date 19th July 2023

About; -
--------
    This module is responsible for talking to gmail api and
    fetching messesses metadata and parsing them.
"""

# Core python packages
import base64
from typing import List
from dataclasses import dataclass, field

# Third party packages
from googleapiclient.errors import HttpError

# Application packages
from src import env_configuration, app_configuration
from src.auth.gmail_auth import GmailAuth
from src.utils.api_logger import ApiLogger
from src.utils.datetime_helper import (
    find_datetime_from_strftime,
    change_format_from_datetime,
)


@dataclass
class MailField:
    id: str = None
    sender: str = None
    receiver: str = None
    subject: str = None
    date: str = None
    snippet: str = None
    body: str = None
    labels: List[str] = field(default_factory=list)


@dataclass
class MailParser:
    connection: GmailAuth = field(default_factory=GmailAuth)

    def parse_msg_attributes(self, headers: dict, mail_field: MailField) -> None:
        """To parse msg attributes.
            payload dictionary contains ‘headers‘, ‘parts‘, ‘filename‘ etc.
            So, we can now easily find headers such as sender, subject, etc. from here.
        Args:
            headers (dict): _description_
            mail_field (MailField): _description_
        """
        for header in headers:
            if header["name"] == "From":
                mail_field.sender = header["value"]

            if header["name"] == "To":
                mail_field.receiver = header["value"]

            if header["name"] == "Subject":
                mail_field.subject = header["value"]

            if header["name"] == "Date":
                # find the datetime format
                dt = find_datetime_from_strftime(header["value"])
                mail_field.date = change_format_from_datetime(
                    dt=dt, date_format="%Y-%m-%d"
                )

    def parse_body(self, parts: list, mail_field: MailField) -> None:
        """
        To parse message body.

        Args:
            parts (list): List of data having messages in parts.
            mail_field (MailField): out data to be consumed later.
        """
        body_message = None

        # Get the data and decode it with base 64 decoder.
        for part in parts:
            body = part.get("body")
            data = body.get("data")
            mimeType = part.get("mimeType")

            # with attachment
            if mimeType == "multipart/related":
                for p in part.get("parts"):
                    body = p.get("body")
                    data = body.get("data")
                    mimeType = p.get("mimeType")
                    if mimeType == "text/plain":
                        body_message = base64.urlsafe_b64decode(data)
                    elif mimeType == "text/html":
                        body_message = base64.urlsafe_b64decode(data)
            # without attachment
            elif mimeType == "text/plain":
                body_message = base64.urlsafe_b64decode(data)
            elif mimeType == "text/html":
                body_message = base64.urlsafe_b64decode(data)

        mail_field.body = body_message  # str(body_message, "utf-8")

        # Now, the data obtained is in lxml. So, we will parse
        # it with BeautifulSoup library
        # soup = BeautifulSoup(decoded_data, "lxml")
        # mail_field.body = soup.body()


@dataclass
class MailReader:
    connection: GmailAuth = field(default_factory=GmailAuth)
    mail_parser: MailParser = MailParser(connection)

    def get_detail(self, message: dict, mail_field: MailField) -> None:
        """
        Get metadata of single message by calling gmail api.

        Args:
            message (dict): message for which metadata needs to be fetched.
            mail_field (MailField): Out data to be consumed later.
        """
        try:
            # Get the message from its id
            email_data = (
                self.connection.service.users()
                .messages()
                .get(userId=env_configuration.USER_ID, id=message["id"], format="full")
                .execute()
            )

            # Fetch labels
            mail_field.labels = email_data["labelIds"]

            # Get value of 'payload' from dictionary 'email_data'
            # This returns a dictionary in which the key ‘payload‘
            # contains the main content of Email in form of Dictionary.
            payload = email_data["payload"]

            # payload dictionary contains ‘headers‘, ‘parts‘, ‘filename‘ etc.
            # So, we can now easily find headers such as sender, subject, etc. from here.
            headers = payload["headers"]

            mail_field.id = message["id"]
            mail_field.snippet = email_data["snippet"]

            self.mail_parser.parse_msg_attributes(
                headers=headers, mail_field=mail_field
            )

            # Temporarily use snippet text for message body
            mail_field.body = mail_field.snippet

            # if payload.get("parts"):
            #     self.mail_parser.parse_body(
            #         parts=payload.get("parts"), mail_field=mail_field
            #     )

        except HttpError as error:
            print(f"Error occurred while parsing email message. {str(error)}")

    def fetch(self) -> None:
        """
        Once connected, we will request a list of messages.

        This will return a list of IDs of the last 100 emails (default value)
        for that Gmail account. We can ask for any number of Emails by
        passing an optional argument ‘maxResults‘.

        Ref: https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.messages.html#list

        Each message resource contains only an `id` and a `threadId`. Additional message details can be fetched using the messages.get method.
        """
        try:
            results = (
                self.connection.service.users()
                .messages()
                .list(
                    userId=env_configuration.USER_ID,
                    maxResults=app_configuration.message_config.max_email_read,
                    labelIds=app_configuration.message_config.labels,
                )
                .execute()
            )
            return results.get("messages", [])
        except HttpError as error:
            print(
                "Error response status code : {0}, reason : {1}".format(
                    error.status_code, error.error_details
                )
            )

    def read(self, db_data: dict) -> None:
        """
        Read gmail data

        Args:
            db_data (dict): Out data in which we store gmail data.
        """
        ApiLogger.log_info("Reading emails from gmail")
        # messages is a list of dictionaries where each dictionary contains a message id
        messages = self.fetch()

        if not messages:
            ApiLogger.log_warning("No messages were found in gmail.")
            return

        ApiLogger.log_info(f"Total emails found : {len(messages)}")

        for message in messages:
            mail_field = MailField()

            self.get_detail(message=message, mail_field=mail_field)

            # Check if email is marked read by reading UNREAD label
            is_read = "UNREAD" not in mail_field.labels

            db_data["email"].append((mail_field.id, is_read))
            # db_data["email_label"].append((mail_field.id, is_read))
            db_data["sender"].append((mail_field.id, mail_field.sender))
            db_data["receiver"].append((mail_field.id, mail_field.receiver))
            db_data["subject"].append((mail_field.id, mail_field.subject))

            if mail_field.body:
                db_data["content"].append((mail_field.id, mail_field.body))
            db_data["date"].append((mail_field.id, mail_field.date))


@dataclass
class LabelReader:
    connection: GmailAuth = field(default_factory=GmailAuth)

    def fetch_labels(self) -> None:
        """
        Fetch label metadata from gmail
        """
        try:
            results = (
                self.connection.service.users()
                .labels()
                .list(userId=env_configuration.USER_ID)
                .execute()
            )
            return results.get("labels", [])
        except HttpError as error:
            ApiLogger.log_error(
                "Error response status code : {0}, reason : {1}".format(
                    error.status_code, error.error_details
                )
            )

    def parse(self, label_data: list) -> None:
        # labels is a list of dictionaries where each dictionary contains a label id
        labels = self.fetch_labels()

        if not labels:
            ApiLogger.log_warning("No labels were found in gmail.")
            return

        ApiLogger.log_info(f"Total labels found : {len(labels)}")

        for label in labels:
            label_data.append((label["id"], label["name"]))
