"""Builds action data from email_rules.json.

@file action_builder.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This module is generates action data to be used later for updating labels in gmail.
"""

# Core python packages
from typing import List
from dataclasses import dataclass, field

# Application packages
from src.rule_engine.action_data import ActionData


@dataclass
class ActionBuilder:
    actions: dict
    action_data: List[ActionData] = field(default_factory=list)

    def get_actions(self) -> None:
        """
        Create action data object from json data in email_rules.json
        """
        for action in self.actions:
            self.action_data.append(ActionData(action["code"], action["label"]))
