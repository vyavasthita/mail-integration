from dataclasses import dataclass
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from src import app_configuration
from src.utils.file_helper import write_to_file, delete_file, check_file_exists
from src.utils.api_logger import ApiLogger
from src import app_configuration


@dataclass
class GmailAuth:
    """
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    auth_credential_json: str = "credentials.json"
    token_json: str = app_configuration.api_config.token_file_path
    creds: Credentials = None
    service: Resource = None

    def check_already_authenticated(self):
        ApiLogger.log_info("Checking if user is already authenticated.")

        # If scopes is modified, we should delete the file token.json
        if check_file_exists(self.token_json):
            ApiLogger.log_debug("Token file is present.")
            self.creds = Credentials.from_authorized_user_file(
                "token.json", scopes=app_configuration.api_config.scope
            )

    def user_log_in(self):
        ApiLogger.log_info("Checking if user login is required.")
        # We check whether or not token json is present
        if not self.creds or not self.creds.valid:
            ApiLogger.log_info("Token does not exist or invalid.")
            # If token does not exist or is invalid, our program will open up
            # the browser and ask for access to the User’s Gmail
            # and save it for next time.
            self.get_token()
            # Save the credentials for the next run
            write_to_file(data=self.creds.to_json(), out_file_path="token.json")

    def get_token(self):
        # token needs to be refreshed
        if self.creds and self.creds.expired and self.creds.refresh_token:
            ApiLogger.log_info(
                "Token expired and refresh token is present. Get token from refresh token."
            )
            self.creds.refresh(Request())
        else:
            ApiLogger.log_info("Run the auth flow using browser.")
            # Open the browser and run auth flow
            self.creds = self.run_auth_flow()

            ApiLogger.log_debug("Post auth flow, delete the credential json file.")
            # Delete credential json file
            delete_file(file_path=self.auth_credential_json)

    def run_auth_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.auth_credential_json, scopes=app_configuration.api_config.scope
        )
        return flow.run_local_server(
            open_browser=False,
            bind_addr=app_configuration.api_config.host,
            port=app_configuration.api_config.port,
        )

    def connect(self):
        ApiLogger.log_info("Connect to Gmail API with access token.")
        # Now, we will connect to the Gmail API with the access token.
        try:
            self.service = build("gmail", "v1", credentials=self.creds)
        except HttpError as error:
            ApiLogger.log_error(f"Failed to connect to Gmail API. {str(error)}")

    def disconnect(self):
        ApiLogger.log_info("Disconnect from Gmail API.")
        self.service.close()


class GmailConnection:
    def __init__(self):
        self.connection = GmailAuth()

    def __enter__(self):
        self.connection.check_already_authenticated()
        self.connection.user_log_in()
        self.connection.connect()

        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.disconnect()
