from typing import List
from dataclasses import dataclass, field
from utils.json_reader import JsonReader


@dataclass
class ApiConfigData:
    host: str = None
    port: int = None
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
            host=self.data["api"]["host"],
            port=self.data["api"]["port"],
            scope=self.data["api"]["scope"],
        )

        msg_config = MessageConfigData(
            max_email_read=self.data["message"]["max_email_read"],
            labels=self.data["message"]["labels"],
        )

        return AppConfigData(api_config=api_config, message_config=msg_config)
