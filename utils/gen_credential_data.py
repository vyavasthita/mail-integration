def gen_data(env_configuration):
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
