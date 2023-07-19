from __future__ import print_function

import os.path
import base64
from bs4 import BeautifulSoup
from dataclasses import dataclass
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from utils.file_helper import write_to_file
from src import configuration


@dataclass
class GmailApi:
    """
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    auth_credential_json: str
    token_json: str = "token.json"
    creds: Credentials = None
    service: Resource = None

    def check_already_authenticated(self):
        # If scopes is modified, we should delete the file token.json
        if os.path.exists(self.token_json):
            self.creds = Credentials.from_authorized_user_file(
                "token.json", scopes=configuration.SCOPES
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

    def run_auth_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.auth_credential_json, scopes=configuration.SCOPES
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

    def fetch_messages(self):
        """
        Once connected, we will request a list of messages.

        This will return a list of IDs of the last 100 emails (default value)
        for that Gmail account. We can ask for any number of Emails by
        passing an optional argument ‘maxResults‘.
        """
        try:
            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    labelIds=["INBOX"],
                    maxResults=configuration.MAX_EMAIL_READ,
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
        for message in self.fetch_messages():
            # Get the message from its id

            email_data = (
                self.service.users()
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )

            # Get value of 'payload' from dictionary 'email_data'
            # This returns a dictionary in which the key ‘payload‘
            # contains the main content of Email in form of Dictionary.
            payload = email_data["payload"]

            # payload dictionary contains ‘headers‘, ‘parts‘, ‘filename‘ etc.
            # So, we can now easily find headers such as sender, subject, etc. from here.
            headers = payload["headers"]

            messaged_id = None
            sender = None
            subject = None
            dateofemail = None

            # Look for Subject and Sender Email in the headers
            for header in headers:
                if header["name"] == "Message-ID":
                    messaged_id = header["value"]

                if header["name"] == "From":
                    sender = header["value"]

                if header["name"] == "Subject":
                    subject = header["value"]

                if header["name"] == "Date":
                    dateofemail = header["value"]

            # Printing the subject, sender's email and message
            print("Message ID: ", message["id"])
            print("Subject: ", subject)
            print("From: ", sender)
            print("Date: ", dateofemail)
            print("********************************************")
