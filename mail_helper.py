"""Main file to start application.

@file mail_helper.py
@author Dilip Kumar Sharma
@date 19th July 2023

About; -
--------
    It is responsible for starting app.

    This class implements arg parser to provide command line arguments.

    This module works as a starting point for our application.
    This modules drives all other operations like validations, intialization, fetching emails and applying rules.
"""
# Core python packages
import os
import json
import argparse
from enum import IntEnum
from dataclasses import dataclass

# Application packages
from src.initialize import (
    init_credential_json,
    create_ftsi,
    check_ftsi,
    validate_auth,
)
from src import environment
from src import create_log_directory
from src.rule_engine.rule_parser import RuleParser
from src.mail_engine.mail_engine import MailEngine
from src.rule_engine.rule_validation import RuleValidation
from src.rule_engine.rule_engine import RuleEngine
from src.utils.api_logger import ApiLogger
from src.utils.file_helper import delete_file
from src.data_layer.db_validation import check_db_connection
from src.initialize import auth, un_auth


class ArgOption(IntEnum):
    VALIDATE = 1
    AUTH = 2
    UNAUTH = 3
    EMAIL = 4
    SHOW_RULES = 5
    APPLY_RULES = 6


class CommandInterface:
    """
    Command line support for the application
    """

    def __init__(self) -> None:
        self.parser = None

    @dataclass
    class Choice:
        option: ArgOption = 1
        rule: str = None

    def initialize_cmd(self) -> None:
        """
        To initialize arg parser
        """
        self.parser = argparse.ArgumentParser(
            prog="mail_helper",
            description="List the cmd parameters for mail helper",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="Thanks for using %(prog)s! :)",
        )

    def create_arguments(self, available_rules: list) -> None:
        """
        To create command line arguments.

        Args:
            available_rules (list): List of rules as defined in email_rules.json
        """
        group = self.parser.add_mutually_exclusive_group()

        group.add_argument(
            "-v",
            "--validate",
            default=False,
            action="store_true",
            help="To do baisc validiation for db connection.",
        )

        group.add_argument(
            "-a",
            "--auth",
            default=False,
            action="store_true",
            help="To do authentication with gmail api.",
        )

        group.add_argument(
            "-u",
            "--unauth",
            default=False,
            action="store_true",
            help="To do un-authentication with gmail api.",
        )

        group.add_argument(
            "-e",
            "--email",
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
            "-ar",
            "--applyrule",
            choices=available_rules,
            help="Apply given rule by its name with value from json key 'rule'",
            nargs=1,
            type=str,
        )

    def get_choice(self, available_rules: list) -> Choice:
        """
        Get the choice selected by user in CMD.

        Args:
            available_rules (list): List of rules as defined in email_rules.json

        Returns:
            Choice: Choice selected by user
        """
        self.create_arguments(available_rules=available_rules)

        choice = CommandInterface.Choice()
        args = self.parser.parse_args()

        if args.validate:
            choice.option = ArgOption.VALIDATE
        elif args.auth:
            choice.option = ArgOption.AUTH
        elif args.unauth:
            choice.option = ArgOption.UNAUTH
        elif args.email:
            choice.option = ArgOption.EMAIL
        elif args.showrules:
            choice.option = ArgOption.SHOW_RULES
            choice.rule = args.showrules[0]
        else:
            choice.option = ArgOption.APPLY_RULES
            choice.rule = args.applyrule[0]

        return choice


class MailHelper:
    def __init__(self) -> None:
        self.rule_parser = None
        self.rule_validation = None

    def initialize(self) -> None:
        """
        Do all initialization related task.
        """
        print("Creating log directory")
        create_log_directory()

        rule_file_path = os.path.join(
            os.getcwd(), "configuration", environment, "email_rules.json"
        )

        self.rule_parser = RuleParser(rule_file_path)
        self.rule_parser.parse()  # Parse email_rules.json file
        self.rule_validation = RuleValidation(self.rule_parser)

        # Read gmail credentials from .env file and write them to a json file because
        # gmail api uses .json file to read credentials.
        init_credential_json()

    def init_cmd(self) -> None:
        """
        To initialize CMD parser.
        """
        print("************************ Mail Helper CLI ************************")

        self.cli.initialize_cmd()

    @check_db_connection
    def validate(self) -> None:
        """
        Triggers all validations.
        Like DB connection and validation related to email_rules.json file.
        """
        # Validate rule parser data
        self.rule_validation.verify_rules()
        print("All validations are done, please proceed.")

    def show_rules(self, rule: str) -> None:
        """
        To show rules available in email_rules.json file.
        Args:
            rule (str): Name of the rule from 'rule' attribute from email_rules.json file.
        """
        ApiLogger.log_info(f"Show rule '{rule}'.")

        if rule == "all":
            print(json.dumps(self.rule_parser.get_all(), indent=1))
        else:
            print(json.dumps(self.rule_parser.get_rule(rule), indent=1))

    @check_db_connection
    @validate_auth
    def start_mail_engine(self) -> None:
        """
        Triggers downloading emails, writing to database and creating full text search indexes.
        Full text search indexes are created post inserting data into tables to improve performance.

        Before triggering the flow, we validate we are connected to db and auth flow is completed.
        """
        ApiLogger.log_debug("Starting Mail Engine.")

        self.mail_engine = MailEngine()
        self.mail_engine.start()

        ApiLogger.log_info("Creating full text search indexes.")
        create_ftsi()

    @check_db_connection
    @validate_auth
    @check_ftsi
    def start_rule_engine(self, rule: str) -> None:
        """
        Triggers applying email rules from email_rules.json.

        Before triggering the flow, we validate we are connected to db, auth flow is completed
        and full text search indexes are created.

        Args:
            rule (str): The selected rule to apply.
        """
        ApiLogger.log_debug("Starting Rule Engine for rulr {rule}.")

        rule_data = self.rule_parser.get_rule(rule)
        rule_engine = RuleEngine()

        rule_engine.start(rule_data)

    def start(self) -> None:
        """
        Starting point for our application.
        """
        self.initialize()
        self.init_cmd()

        ApiLogger.log_info("Get the choice selected by user from command line.")
        choice = self.cli.get_choice(self.rule_parser.get_available_rules())

        self.validate()

        if choice.option == ArgOption.AUTH:
            auth()
        if choice.option == ArgOption.UNAUTH:
            un_auth()
        elif choice.option == ArgOption.EMAIL:
            self.start_mail_engine()
        elif choice.option == ArgOption.SHOW_RULES:
            self.show_rules(choice.rule)
        elif choice.option == ArgOption.APPLY_RULES:
            self.start_rule_engine(choice.rule)

    def clean_up(self) -> None:
        """
        Do necessary clean up required.
        """
        pass  # TBD


if __name__ == "__main__":
    mail_helper = MailHelper()

    mail_helper.cli = CommandInterface()
    mail_helper.start()
    mail_helper.clean_up()
    print("*********** Application Ended *********************")
