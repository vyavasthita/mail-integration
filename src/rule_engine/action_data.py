"""Action data from email_rules.json.

@file action_data.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This module is represents actions defined in email_rules.json
"""
# Core python packages
from dataclasses import dataclass
from enum import IntEnum


class ActionCode(IntEnum):
    MOVE = 1
    READ = 2
    UNREAD = 3


@dataclass
class ActionData:
    code: int = None
    label: str = None
