"""Rule engine for applying rules

@file rule_engine.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This module drives applying rules as per rules defined in email_rules.json.
"""
# Core python packages
from typing import List
from dataclasses import dataclass, field

# Application packages
from src.rule_engine.query_builder import AnyQueryBuilder, AllQueryBuilder
from src.rule_engine.action_builder import ActionBuilder
from src.rule_engine.action_data import ActionData, ActionCode
from src.utils.api_logger import ApiLogger
from src.data_layer.mail_dao import MailDao
from src.api.api_request import ApiRequest


@dataclass
class RuleEngine:
    rule_data: dict = field(default_factory=dict)
    action_data: List[ActionData] = field(default_factory=list)

    def build_query(self, predicate: str, conditions: dict) -> str:
        """
        Build single query as per all conditions defined in email_rules.json

        Args:
            predicate (str): 'All' or 'Any'
            conditions (dict): All conditions for which query needs to be generated.

        Returns:
            str: Query string
        """
        if predicate == "all":
            all_query_builder = AllQueryBuilder()
            return all_query_builder.build_all_predicate(conditions)
        elif predicate == "any":
            any_query_builder = AnyQueryBuilder()
            return any_query_builder.build_any_predicate(conditions)

    def build_actions(self, actions: dict) -> None:
        """
        Build actions as per the rules defined in email_rules.json.

        Args:
            actions (dict): All actions to be applied as per email_rules.json.
        """
        action_builder = ActionBuilder(actions, self.action_data)
        action_builder.get_actions()

    def build(self, selected_rule_data: dict) -> None:
        """
        Build all conditions and actions in email_rules.json

        Args:
            selected_rule_data (dict): Selected rule from email_rules.json.
        """
        query = self.build_query(
            selected_rule_data["predicate"], selected_rule_data["conditions"]
        )

        self.build_actions(selected_rule_data["actions"])

        return query

    def start(self, selected_rule_data: dict) -> None:
        """
        Triggers applying rules.

        Args:
            selected_rule_data (dict): _description_
        """
        api_request = ApiRequest()
        api_request.update_label( MailDao.read(self.build(selected_rule_data)), self.action_data)
