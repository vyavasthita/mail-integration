from src.gmail_api import GmailApi
from src.initialize import init_rule_parser, init_credential_json


def init():
    init_rule_parser()
    init_credential_json()


init()

gmail_api = GmailApi()
gmail_api.check_already_authenticated()
gmail_api.user_log_in()
gmail_api.connect()

for mail in gmail_api.parse_messages():
    # Printing the subject, sender's email and message
    print("Message ID: ", mail.message_id)
    print("From: ", mail.sender)
    print("To: ", mail.receiver)
    print("Subject: ", mail.subject)
    print("Date: ", mail.date)
    if mail.body:
        print("Body: ", mail.body)
    print("Labels: ", mail.labels)
    print("********************************************")
