"""To Initialize application.

@file gen_credential_data.py
@author Dilip Kumar Sharma
@date 19 July 2023

About; -
--------
    Read gmail credentials from .env file and write them to a json file because
    gmail api uses .json file to read credentials.
"""
# Application packages
from src.utils.api_logger import ApiLogger


def gen_data(env_configuration) -> dict:
    """Generate json from .env file

    Args:
        env_configuration (_type_): _description_

    Returns:
        dict: Generated dict object to be written to json file.
    """
    ApiLogger.log_debug("Creating credential json data from environment variables.")

    data = dict()

    installed_data = dict()

    installed_data["client_id"] = env_configuration.CLIENT_ID
    installed_data["project_id"] = env_configuration.PROJECT_ID
    installed_data["auth_uri"] = env_configuration.AUTH_URI
    installed_data["token_uri"] = env_configuration.TOKEN_URI
    installed_data[
        "auth_provider_x509_cert_url"
    ] = env_configuration.AUTH_PROVIDER_X509_CERT_URL
    installed_data["client_secret"] = env_configuration.CLIENT_SECRET

    redirect_uris = list()
    redirect_uris.append(env_configuration.REDIRECT_URIS)

    installed_data["redirect_uris"] = redirect_uris

    data["installed"] = installed_data

    return data
