"""OAuth to gmail api.

@file auth.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This modules checks oauth connection with gmail api.
"""
# Application packages
from src import app_configuration, env_configuration
from src.utils.file_helper import check_file_exists, delete_file
from src.auth.gmail_auth import GmailConnection
from src.utils.json_reader import JsonReader
from src.utils.api_logger import ApiLogger


class Auth:
    def is_authenticated(self) -> bool:
        """
        This method check the presence of token.json file.
        If file present then we have refreash token available in that file
        and hence we mark it as authenticated.

        Returns:
            bool: Whether or not authenticated.
        """
        ApiLogger.log_info("Checking if user is already authenticated.")
        return (
            True
            if check_file_exists(app_configuration.api_config.token_file_path)
            else False
        )

    def un_authenticate(self) -> None:
        """
        Un authenticate by deleting token.json file.
        Auth flow when runs next time, it will create token.json file again.
        """
        if self.is_authenticated():
            delete_file(app_configuration.api_config.token_file_path)
            ApiLogger.log_info("User is unauthenticated successfully.")
        else:
            ApiLogger.log_info("User is already un-authenticated.")

    def start(self) -> None:
        """
        Start Auth flow if not already authenticated.
        """
        if self.is_authenticated():
            ApiLogger.log_info("User is already authenticated.")
        else:
            with GmailConnection() as connection:  # do auth flow
                pass

        # Read refresh token from token.json file and save in memory
        # This will be used later when we need access token to call RestApi
        token_data = None
        json_reader = JsonReader(app_configuration.api_config.token_file_path)

        try:
            token_data = json_reader.read()
        except ValueError as error:
            ApiLogger.log_critical("Failed to parse App Config File.")

        env_configuration.REFRESH_TOKEN = token_data["refresh_token"]
