"""OAuth to gmail api.

@file connection.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This modules makes connection to gmail api using oauth.
"""

# Third party packages
from requests_oauthlib import OAuth2Session  # Authenticating with OAuth2 in Requests

# Application packages
from src import env_configuration
from src import app_configuration


class AuthConnection:
    def __init__(self) -> None:
        self.session = OAuth2Session(
            client_id=env_configuration.CLIENT_ID,
            scope=app_configuration.api_config.scope,
            redirect_uri=env_configuration.REDIRECT_URIS,
        )

    def __enter__(self) -> None:
        extra = {
            "client_id": env_configuration.CLIENT_ID,
            "client_secret": env_configuration.CLIENT_SECRET,
        }

        self.session.refresh_token(
            token_url=env_configuration.TOKEN_URI,
            refresh_token=env_configuration.REFRESH_TOKEN,
            **extra
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
