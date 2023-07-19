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
    RULE_PARSER_FILE_PATH = "config/email_rules.json"

    def __init__(self):
        self.data = None
        self.rules = None
        self.read_configuration()

    def read_configuration(self):
        if os.path.exists(JsonRuleParser.RULE_PARSER_FILE_PATH):
            with open(JsonRuleParser.RULE_PARSER_FILE_PATH) as json_file_object:
                self.rules = json.load(json_file_object)
        else:
            raise ValueError(
                "Connection configuration file path '{}' is invalid.".format(
                    JsonRuleParser.RULE_PARSER_FILE_PATH
                )
            )

    def parse(self):
        pass

    def get_rule(self, rule_name):
        for rule in self.rules:
            if rule_name == rule.get("rule"):
                return json.dumps(self.rules, indent=1)
