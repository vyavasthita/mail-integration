def gen_data(configuration):
    data = dict()

    installed_data = dict()

    installed_data["client_id"] = configuration.CLIENT_ID
    installed_data["project_id"] = configuration.PROJECT_ID
    installed_data["auth_uri"] = configuration.AUTH_URI
    installed_data["token_uri"] = configuration.TOKEN_URI
    installed_data[
        "auth_provider_x509_cert_url"
    ] = configuration.AUTH_PROVIDER_X509_CERT_URL
    installed_data["client_secret"] = configuration.CLIENT_SECRET

    redirect_uris = list()
    redirect_uris.append(configuration.REDIRECT_URIS)

    installed_data["redirect_uris"] = redirect_uris

    data["installed"] = installed_data

    return data
