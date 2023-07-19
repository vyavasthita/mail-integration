from src.gmail_api import ApiConnection, Email, Label
from src.initialize import init_rule_parser, init_credential_json
from src.cli import get_choice
from src.db_dao import EmailFetchDao


def init():
    init_rule_parser()
    init_credential_json()


init()


def fetch_emails():
    api_connection = ApiConnection()
    emails = Email(api_connection=api_connection)
    labels = Label(api_connection=api_connection)

    api_connection.check_already_authenticated()
    api_connection.user_log_in()
    api_connection.connect()

    db_data = dict()
    db_data["receiver"] = list()
    db_data["message"] = list()
    db_data["sender"] = list()
    db_data["subject"] = list()
    db_data["date_info"] = list()

    emails.parse(db_data=db_data)

    label_data = list()
    labels.parse(label_data)  # pass by object reference

    api_connection.disconnect()  # Todo: Context Manager ?

    db_data["label"] = label_data

    EmailFetchDao.add_emails(db_data=db_data)


choice = get_choice()

if choice.emails:
    fetch_emails()
