import os
import json
import argparse
from enum import IntEnum
from dataclasses import dataclass
from src import environment
from src.initialize import init_credential_json, create_ftsi
from src import create_log_directory
from src.rule_engine.rule_parser import RuleParser
from src.mail_engine.mail_engine import MailEngine
from src.rule_engine.rule_engine import RuleEngine
from src.utils.api_logger import ApiLogger
from src.data_layer.db_validation import check_db_connection


class ArgOption(IntEnum):
    VALIDATE = 1
    FETCH_EMAIL = 2
    SHOW_RULES = 3
    APPLY_RULES = 4


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
            "-v",
            "--validate",
            default=False,
            action="store_true",
            help="To do baisc validiation like db connection is established.",
        )

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

        if args.validate:
            choice.option = ArgOption.VALIDATE
        elif args.emails:
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
        print("Creating log directory")
        create_log_directory()

        rule_file_path = os.path.join(
            os.getcwd(), "config", environment, "email_rules.json"
        )

        self.cli = CommandInterface()
        self.rule_parser = RuleParser(rule_file_path)

    def initialize(self):
        print("************************ Mail Helper CLI ************************")
        init_credential_json()
        self.rule_parser.parse()
        self.cli.initialize_cmd()

    @check_db_connection
    def validate(self):
        print("All validations are done, please proceed.")

    def show_rules(self, rule: str):
        ApiLogger.log_info(f"Show rule {rule}.")

        if rule == "all":
            print(json.dumps(self.rule_parser.get_all(), indent=1))
        else:
            print(json.dumps(self.rule_parser.get_rule(rule), indent=1))

    @check_db_connection
    @create_ftsi
    def start_mail_engine(self):
        ApiLogger.log_debug("Initializing credential json.")
        self.mail_engine = MailEngine()

        self.mail_engine.start()

    @check_db_connection
    @create_ftsi
    def start_rule_engine(self, rule: str):
        rule_data = self.rule_parser.get_rule(rule)
        rule_engine = RuleEngine()

        # rule_engine.start(rule_data)

    def start(self):
        choice = self.cli.get_choice(self.rule_parser.get_available_rules())

        if choice.option == ArgOption.VALIDATE:
            self.validate()
        elif choice.option == ArgOption.FETCH_EMAIL:
            self.start_mail_engine()
        elif choice.option == ArgOption.SHOW_RULES:
            self.show_rules(choice.rule)
        else:
            self.start_rule_engine(choice.rule)


if __name__ == "__main__":
    mail_helper = MailHelper()

    mail_helper.initialize()
    mail_helper.start()
