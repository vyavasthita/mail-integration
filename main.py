from src.gmail_api import ApiConnection, Email, Label
from src.initialize import init_rule_parser, init_credential_json
from src.cli import get_choice
from src.db_init import DBConnection


def init():
    init_rule_parser()
    init_credential_json()


init()

# Connect to DB
with DBConnection() as connection:
    connection.cursor.execute("SELECT VERSION()")
    row = connection.cursor.fetchone()
    print("server version:", row[0])


def fetch_emails():
    api_connection = ApiConnection()
    emails = Email(api_connection=api_connection)
    labels = Label(api_connection=api_connection)

    api_connection.check_already_authenticated()
    api_connection.user_log_in()
    api_connection.connect()

    for mail in emails.parse():
        # Printing the subject, sender's email and message
        print("Message ID: ", mail.id)
        print("From: ", mail.sender)
        print("To: ", mail.receiver)
        print("Subject: ", mail.subject)
        print("Date: ", mail.date)
        if mail.body:
            print("Body: ", mail.body)
        print("Labels: ", mail.labels)
        print("********************************************")

    for label in labels.parse():
        # Printing the subject, sender's email and message
        print("Lable ID: ", label.id)
        print("Name: ", label.name)
        print("********************************************")

    api_connection.disconnect()  # Todo: Context Manager ?


choice = get_choice()

if choice.emails:
    fetch_emails()
