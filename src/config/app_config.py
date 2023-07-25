"""Application configuration.

@file app_config.py
@author Dilip Kumar Sharma
@date 20 July 2023

About; -
--------
    To read application configuration from app_config.json file.
"""

# Core python packages
import sys
from typing import List
from dataclasses import dataclass, field

# Application packages
from src.utils.json_reader import JsonReader
from src.utils.api_logger import ApiLogger


@dataclass
class ApiConfigData:
    token_file_path: str = None
    host: str = None
    port: int = None
    index_sp_name: str = None
    scope: List[str] = field(default_factory=list)


@dataclass
class MessageConfigData:
    max_email_read: int = 100
    labels: List[str] = field(default_factory=list)


@dataclass
class AppConfigData:
    api_config: ApiConfigData = field(default_factory=ApiConfigData)
    message_config: MessageConfigData = field(default_factory=MessageConfigData)


@dataclass
class AppConfigParser:
    file_path: str
    data: dict = None

    def parse(self) -> ApiConfigData:
        """
        Parse json file.

        Returns:
            ApiConfigData: Configuration data
        """
        json_reader = JsonReader(self.file_path)
        try:
            self.data = json_reader.read()
        except ValueError:
            ApiLogger.log_critical("Failed to parse App Config File. Exiting...")
            sys.exit(0)

        api_config = ApiConfigData(
            token_file_path=self.data["api"]["token_file_path"],
            host=self.data["api"]["host"],
            port=self.data["api"]["port"],
            index_sp_name=self.data["api"]["index_sp_name"],
            scope=self.data["api"]["scope"],
        )

        msg_config = MessageConfigData(
            max_email_read=self.data["message"]["max_email_read"],
            labels=self.data["message"]["labels"],
        )

        return AppConfigData(api_config=api_config, message_config=msg_config)
