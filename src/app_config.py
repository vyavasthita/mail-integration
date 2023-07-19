from typing import List
from dataclasses import dataclass, field
from utils.json_reader import JsonReader


@dataclass
class AppConfigData:
    max_email_read: int = 100
    labels: List[str] = field(default_factory=list)


@dataclass
class AppConfigParser:
    file_path: str
    data: dict = None

    def parse(self):
        json_reader = JsonReader(self.file_path)
        self.data = json_reader.read()
        return AppConfigData(max_email_read=self.data["MAX_EMAIL_READ"], labels=self.data["labels"])
