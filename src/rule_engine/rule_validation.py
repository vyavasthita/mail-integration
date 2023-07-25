"""Rule validation for rule defined in email_rule.json

@file rule_validation.py
@author Dilip Kumar Sharma
@date 19th July 2023

About; -
--------
    Parses email_rules.json.
"""
# Core python packages
import sys
from dataclasses import dataclass, field

# Application packages
from src.data_layer.mail_dao import MailDao
from src.utils.api_logger import ApiLogger
from src.rule_engine.rule_parser import RuleParser


@dataclass
class RuleValidation:
    rule_parser: RuleParser = field(default_factory=RuleParser)
    available_labels: list = field(default_factory=list)

    def set_available_labels(self) -> None:
        query = """SELECT label_id FROM label"""

        self.available_labels = [result[0] for result in MailDao.read(query)]

    def is_valid_labels(self, labels: dict) -> None:
        """
        Check if labels from email_rules are valid as per labels from gmail.

        When we are running application for the first time to fetch emails, we do not have labels
        in our database and hence we should not do validation.
        Post first run, we will have labels in database and we can do validation

        Args:
            labels (dict): Labels to check for.
        """
        if self.available_labels:
            for rule, labels in labels.items():
                ApiLogger.log_info(f"Verifying labels for rule {rule}.")

                for label in labels:
                    if label not in self.available_labels:
                        ApiLogger.log_error(
                            f"Invalid label '{label}' found for rule '{rule}' in rule parser. Available labels -> {self.available_labels}."
                        )
                        sys.exit(0)

    def verify_rules(self) -> None:
        """
        Verify rules given in email_rules.json
        """
        # Verify labels
        self.set_available_labels()
        # self.is_valid_labels(self.rule_parser.get_labels())
