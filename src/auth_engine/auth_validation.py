from src import app_configuration, env_configuration
from src.auth_engine.gmail_auth import GmailConnection
from src.utils.file_helper import check_file_exists, delete_file
from src.utils.json_reader import JsonReader
from src import app_configuration
from src.utils.api_logger import ApiLogger


class AuthValidation:
    def is_authenticated(self):
        ApiLogger.log_info("Checking if user is already authenticated.")
        return (
            True
            if check_file_exists(app_configuration.api_config.token_file_path)
            else False
        )

    def un_authenticate(self):
        if self.is_authenticated():
            delete_file(app_configuration.api_config.token_file_path)
            ApiLogger.log_info("User is unauthenticated successfully.")
        else:
            ApiLogger.log_info("User is already un-authenticated.")

    def start(self):
        if self.is_authenticated():
            ApiLogger.log_info("User is already authenticated.")
        else:
            with GmailConnection() as connection:
                pass

        # Read refresh token from token.json file and save in memory
        # This will be used later when we need access token to call RestApi
        json_reader = JsonReader(app_configuration.api_config.token_file_path)
        token_data = json_reader.read()
        env_configuration.REFRESH_TOKEN = token_data["refresh_token"]
