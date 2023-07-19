import os
from src import env_configuration, environment
from src.gmail_api import GmailApi
from utils.gen_credential_data import gen_data
from utils.file_helper import write_to_json
from src.rule_parser import RuleParser


credential_out_json_file_path = "credentials.json"
rule_parser_file_path = os.path.join(
    os.getcwd(), "config", environment, "email_rules.json"
)


write_to_json(
    json_string=gen_data(env_configuration=env_configuration),
    out_file_path=credential_out_json_file_path,
)

gmail_api = GmailApi(auth_credential_json=credential_out_json_file_path)
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


# parse rule parser
parser = RuleParser(file_path=rule_parser_file_path)
data = parser.parse()

print(data)
