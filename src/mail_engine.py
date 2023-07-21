from src.gmail_api import ApiConnection, Email, Label
from src.db_dao import EmailFetchDao
from utils.api_logger import ApiLogger


class MailEngine:
    def __init__(self) -> None:
        pass

    def fetch_emails(self):
        api_connection = ApiConnection()

        emails = Email(api_connection=api_connection)

        labels = Label(api_connection=api_connection)

        api_connection.check_already_authenticated()
        api_connection.user_log_in()
        api_connection.connect()

        db_data = dict()

        db_data["email"] = list()
        # db_data["email_label"] = list()
        db_data["sender"] = list()
        db_data["receiver"] = list()
        db_data["subject"] = list()
        db_data["content"] = list()
        db_data["date"] = list()

        ApiLogger.log_debug("Fetching emails.")
        emails.parse(db_data=db_data)

        label_data = list()

        ApiLogger.log_debug("Fetching labels.")
        labels.parse(label_data)  # pass by object reference

        api_connection.disconnect()  # Todo: Context Manager ?

        db_data["label"] = label_data

        EmailFetchDao.add_emails(db_data=db_data)
