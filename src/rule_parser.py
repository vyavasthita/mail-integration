from abc import ABC, abstractmethod
import os
import json


class RuleParser(ABC):
    @abstractmethod
    def read_configuration(self):
        raise NotImplementedError(
            "Abstract method 'read_configuration' needs implementation."
        )


class JsonRuleParser(RuleParser):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rules = None
        self.read_configuration()

    def read_configuration(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as json_file_object:
                    self.rules = json.load(json_file_object)
            except ValueError as error:
                print(f"Invalid Json File. {self.file_path}")
        else:
            raise ValueError(
                "Connection configuration file path '{}' is invalid.".format(
                    self.file_path
                )
            )

    def parse(self):
        return self.rules

    def get_rule(self, rule_name):
        for rule in self.rules:
            if rule_name == rule.get("rule"):
                return json.dumps(self.rules, indent=1)
