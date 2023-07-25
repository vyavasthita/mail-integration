"""Email data.

@file mail_data.py
@author Dilip Kumar Sharma
@date 20th July 2023

About; -
--------
    Represents email data to be shared across modules.
"""
# Core python packages
from dataclasses import dataclass, field


@dataclass
class MailData:
    query_string: str
    query_data: list = field(default_factory=list)
