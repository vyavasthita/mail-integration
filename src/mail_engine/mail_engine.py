from src.auth.gmail_auth import GmailConnection
from src.mail_engine.mail_reader import MailReader, LabelReader
from src.mail_engine.mail_data_builder import MailDataBuilder
from src.utils.api_logger import ApiLogger


# @dataclass
class MailEngine:
    def __init__(self) -> None:
        self.data = dict()

        self.mail_data = list()
        self.mail_data_builder = MailDataBuilder(self.mail_data, self.data)

    def init_data(self):
        self.data["email"] = list()
        self.data["email_label"] = list()
        self.data["sender"] = list()
        self.data["receiver"] = list()
        self.data["subject"] = list()
        self.data["content"] = list()
        self.data["date"] = list()

    def start(self):
        label_data = list()
        self.init_data()

        with GmailConnection() as connection:
            mail_reader = MailReader(connection)
            label_reader = LabelReader(connection=connection)

            ApiLogger.log_debug("Fetching emails.")
            mail_reader.read(db_data=self.data)  # pass by object reference

            ApiLogger.log_debug("Fetching labels.")
            label_reader.parse(label_data)  # pass by object reference

        self.data["label"] = label_data

        self.mail_data_builder.construct_write_data()
        self.mail_data_builder.write_to_db()
