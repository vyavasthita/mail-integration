# Authenticating with OAuth2 in Requests
from requests_oauthlib import OAuth2Session
from src import env_configuration
from src import app_configuration


class ApiAuth:
    def __init__(self):
        self.session = OAuth2Session(
            client_id=env_configuration.CLIENT_ID,
            scope=app_configuration.api_config.scope,
            redirect_uri=env_configuration.REDIRECT_URIS,
        )

    def __enter__(self):
        extra = {
            "client_id": env_configuration.CLIENT_ID,
            "client_secret": env_configuration.CLIENT_SECRET,
        }

        self.session.refresh_token(
            token_url=env_configuration.TOKEN_URI,
            refresh_token=env_configuration.REFRESH_TOKEN,
            **extra
        )
        print("********* getting token ***********")
        print(env_configuration.REFRESH_TOKEN)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
