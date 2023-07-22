from dataclasses import dataclass, field
from src.utils.json_reader import JsonReader
from src.utils.api_logger import ApiLogger


@dataclass
class RuleParser:
    file_path: str
    data: dict = field(default_factory=dict)

    def parse(self):
        ApiLogger.log_debug("Reading rule parsing json configuration.")
        json_reader = JsonReader(self.file_path)
        self.data = json_reader.read()

    def get_all(self):
        return self.data

    def get_available_rules(self):
        return [rule_data["rule"] for rule_data in self.data]

    def get_rule(self, rule: str):
        for rule_data in self.data:
            if rule_data.get("rule") == rule:
                return rule_data
