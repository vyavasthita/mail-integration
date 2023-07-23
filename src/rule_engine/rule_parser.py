"""Parser for email_rules.json.

@file rule_parser.py
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
from src.utils.json_reader import JsonReader
from src.utils.api_logger import ApiLogger


@dataclass
class RuleParser:
    file_path: str
    data: dict = field(default_factory=dict)

    def parse(self) -> None:
        """
        Parse email_rules.json
        """
        ApiLogger.log_debug("Reading rule parsing json configuration.")
        json_reader = JsonReader(self.file_path)

        try:
            self.data = json_reader.read()
        except ValueError as error:
            ApiLogger.log_critical("Failed to parse App Config File. Exiting...")
            sys.exit(0)

    def get_all(self) -> dict:
        """
        Get all data dict from email_rules.json

        Returns:
            dict: Data dict
        """
        return self.data

    def get_available_rules(self) -> list:
        """
        Get available rules from email_rules.json

        Returns:
            list: List of rules
        """
        return [rule_data["rule"] for rule_data in self.data]

    def get_rule(self, rule: str) -> dict:
        """
        Selected rule from email_rules.json

        Args:
            rule (str): Rule to be searched for.

        Returns:
            dict: Rule dict data
        """
        for rule_data in self.data:
            if rule_data.get("rule") == rule:
                return rule_data

    def get_labels(self) -> dict:
        """
        Get all labels defined in all rules in email_rules.json


        Returns:
            dict: Dict of rules
        """
        return {
            rule_data["rule"]: [
                action["label"].upper() for action in rule_data["actions"]
            ]
            for rule_data in self.data
        }
