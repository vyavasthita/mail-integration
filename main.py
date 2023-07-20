import json
from src.gmail_api import ApiConnection, Email, Label
from src.initialize import init_rule_parser, init_credential_json
from src.cli import ArgOption, get_choice
from src.db_dao import EmailFetchDao, SPDao
from src import create_log_directory
from src.query_builder import QueryBuilder
from utils.api_logger import ApiLogger


print("Creating log directory")
create_log_directory()

ApiLogger.log_debug("Initializing credential json.")
init_credential_json()

rules_data = init_rule_parser()


def get_available_rules():
    return [rule_data["rule"] for rule_data in rules_data]


def get_rule(rule: str):
    for rule_data in rules_data:
        if rule_data.get("rule") == rule:
            return rule_data


def fetch_emails():
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


def create_ftsi():
    ApiLogger.log_info("Creating full text search indexes.")
    SPDao.call_sp("create_fti")


def read_emails():
    ApiLogger.log_info("Fetch emails.")
    fetch_emails()
    create_ftsi()


def show_rules(rule: str):
    ApiLogger.log_info(f"Show rule {rule}.")

    if rule == "all":
        print(json.dumps(rules_data, indent=1))
    else:
        rule_data = get_rule(rule)
        print(json.dumps(rule_data, indent=1))


def apply_rule(rule: str):
    ApiLogger.log_info(f"Applying rule {rule}.")

    rule_data = get_rule(rule)
    query_builer = QueryBuilder(rule_data)
    query_builer.build()


choice = get_choice(get_available_rules())

if choice.option == ArgOption.FETCH_EMAIL:
    read_emails()
elif choice.option == ArgOption.SHOW_RULES:
    show_rules(choice.rule)
else:
    apply_rule(choice.rule)
