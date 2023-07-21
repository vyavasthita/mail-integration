from dataclasses import dataclass
from src.utils.json_reader import JsonReader


@dataclass
class RuleParser:
    file_path: str

    def parse(self):
        json_reader = JsonReader(self.file_path)
        return json_reader.read()
