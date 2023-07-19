import os
import json
from dataclasses import dataclass
from utils.json_reader import JsonReader


@dataclass
class RuleParser:
    file_path: str
    data: dict = None

    def parse(self):
        json_reader = JsonReader(self.file_path)
        self.data = json_reader.read()
        return self.data

    def get_rule(self, rule_name):
        for rule in self.data:
            if rule_name == rule.get("rule"):
                return json.dumps(self.data, indent=1)
