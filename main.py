from src import configuration
from src.gmail_api import GmailApi
from utils.gen_credential_data import gen_data
from utils.file_helper import write_to_json

out_json_file_path = "credentials.json"
json_string = gen_data(configuration=configuration)


write_to_json(
    json_string=gen_data(configuration=configuration),
    out_file_path=out_json_file_path,
)

gmail_api = GmailApi(auth_credential_json=out_json_file_path)
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
