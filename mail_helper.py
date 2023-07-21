import json
import argparse
from enum import IntEnum
from dataclasses import dataclass
from src.initialize import init_credential_json
from src.db_dao import SPDao
from src import create_log_directory
from src.rule_data import RuleData
from src.mail_engine import MailEngine
from src.rule_engine import RuleEngine
from utils.api_logger import ApiLogger


class ArgOption(IntEnum):
    FETCH_EMAIL = 1
    SHOW_RULES = 2
    APPLY_RULES = 3


class CommandInterface:
    def __init__(self) -> None:
        self.parser = None

    @dataclass
    class Choice:
        option: ArgOption = 1
        rule: str = None

    def initialize_cmd(self):
        self.parser = argparse.ArgumentParser(
            prog="mail_helper",
            description="List the cmd parameters for mail helper",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="Thanks for using %(prog)s! :)",
        )

    def read_arguments(self, available_rules: list):
        group = self.parser.add_mutually_exclusive_group()

        group.add_argument(
            "-e",
            "--emails",
            default=False,
            action="store_true",
            help="To fetch emails from Gmail",
        )

        group.add_argument(
            "-s",
            "--showrules",
            choices=available_rules + ["all"],
            help="Show all the available rules. Select all for all rules or select a particular rule",
            nargs=1,
            type=str,
        )

        group.add_argument(
            "-a",
            "--applyrule",
            choices=available_rules,
            help="Apply given rule by its name with value from json key 'rule'",
            nargs=1,
            type=str,
        )

    def get_choice(self, available_rules: list) -> Choice:
        self.read_arguments(available_rules=available_rules)

        choice = CommandInterface.Choice()
        args = self.parser.parse_args()

        if args.emails:
            choice.option = ArgOption.FETCH_EMAIL
        elif args.showrules:
            choice.option = ArgOption.SHOW_RULES
            choice.rule = args.showrules[0]
        else:
            choice.option = ArgOption.APPLY_RULES
            choice.rule = args.applyrule[0]

        return choice


class MailHelper:
    def __init__(self) -> None:
        self.cli = CommandInterface()
        self.rule_data = RuleData()
        self.mail_engine = MailEngine()
        self.rule_engine = RuleEngine()

    def initialize(self):
        print("Creating log directory")
        create_log_directory()

        print(
            "************************** Mail Helper CLI **********************************************"
        )
        self.cli.initialize_cmd()

    def show_rules(self, rule: str):
        ApiLogger.log_info(f"Show rule {rule}.")

        if rule == "all":
            print(json.dumps(self.rule_data.get_all(), indent=1))
        else:
            print(json.dumps(self.rule_data.get_rule(rule), indent=1))

    def create_ftsi(self):
        ApiLogger.log_info(
            "Calling stored procedure to create full text search indexes."
        )
        SPDao.call_sp("create_fti")

    def start(self):
        choice = self.cli.get_choice(self.rule_data.get_available_rules())

        if choice.option == ArgOption.FETCH_EMAIL:
            ApiLogger.log_debug("Initializing credential json.")
            init_credential_json()
            self.mail_engine.fetch_emails()
            self.create_ftsi()
        elif choice.option == ArgOption.SHOW_RULES:
            self.show_rules(choice.rule)
        else:
            self.rule_engine.apply_rule(choice.rule)


if __name__ == "__main__":
    mail_helper = MailHelper()

    mail_helper.initialize()
    mail_helper.start()
