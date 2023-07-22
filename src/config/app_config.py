from typing import List
from dataclasses import dataclass, field
from src.utils.json_reader import JsonReader


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

    def parse(self):
        json_reader = JsonReader(self.file_path)
        self.data = json_reader.read()

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
