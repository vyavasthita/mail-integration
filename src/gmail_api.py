from __future__ import print_function

import os.path
import base64
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass, field
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from utils.file_helper import write_to_file, delete_file
from src import env_configuration, app_configuration


@dataclass
class MailField:
    message_id: str = None
    sender: str = None
    receiver: str = None
    subject: str = None
    date: str = None
    body: str = None
    labels: List[str] = field(default_factory=list)


@dataclass
class GmailApi:
    """
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    auth_credential_json: str = "credentials.json"
    token_json: str = "token.json"
    creds: Credentials = None
    service: Resource = None
    mails: List[MailField] = field(default_factory=list)

    def check_already_authenticated(self):
        # If scopes is modified, we should delete the file token.json
        if os.path.exists(self.token_json):
            self.creds = Credentials.from_authorized_user_file(
                "token.json", scopes=app_configuration.api_config.scope
            )

    def user_log_in(self):
        # We check whether or not token json is present
        if not self.creds or not self.creds.valid:
            # If token does not exist or is invalid, our program will open up
            # the browser and ask for access to the User’s Gmail
            # and save it for next time.
            self.get_token()
            # Save the credentials for the next run
            write_to_file(data=self.creds.to_json(), out_file_path="token.json")

    def get_token(self):
        # token needs to be refreshed
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            # Open the browser and run auth flow
            self.creds = self.run_auth_flow()

            # Delete credential json file
            delete_file(file_path=self.auth_credential_json)

    def run_auth_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.auth_credential_json, scopes=app_configuration.api_config.scope
        )
        return flow.run_local_server(port=0)

    def connect(self):
        # Now, we will connect to the Gmail API with the access token.
        try:
            self.service = build("gmail", "v1", credentials=self.creds)
        except HttpError as error:
            print(f"Failed to connect. {str(error)}")

    def disconnect(self):
        self.service.close()

    def parse_msg_attributes(self, headers: dict, mail_field: MailField):
        # payload dictionary contains ‘headers‘, ‘parts‘, ‘filename‘ etc.
        # So, we can now easily find headers such as sender, subject, etc. from here.
        for header in headers:
            if header["name"] == "From":
                mail_field.sender = header["value"]

            if header["name"] == "To":
                mail_field.receiver = header["value"]

            if header["name"] == "Subject":
                mail_field.subject = header["value"]

            if header["name"] == "Date":
                mail_field.date = header["value"]

    def parse_body(self, parts, mail_field: MailField):
        # Get the data and decode it with base 64 decoder.
        if parts["body"].get("data"):
            data = parts["body"]["data"]
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data, "lxml")
            mail_field.body = soup.body()

    def get_message_detail(self, message):
        mail_field = MailField()

        try:
            # Get the message from its id
            email_data = (
                self.service.users()
                .messages()
                .get(userId=env_configuration.USER_ID, id=message["id"])
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

            mail_field.message_id = message["id"]

            self.parse_msg_attributes(headers=headers, mail_field=mail_field)

            if payload.get("parts"):
                self.parse_body(parts=payload.get("parts")[0], mail_field=mail_field)

            self.mails.append(mail_field)

        except HttpError as error:
            print(f"Error occurred while parsing email message. {str(error)}")

    def fetch_messages(self):
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
                self.service.users()
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

    def parse_messages(self):
        # messages is a list of dictionaries where each dictionary contains a message id
        messages = self.fetch_messages()

        if not messages:
            print("No messages were found.")
            return

        for message in self.fetch_messages():
            self.get_message_detail(message=message)

        return self.mails
