from src.initialize import init_rule_parser


class RuleData:
    def __init__(self) -> None:
        self.rules_data = init_rule_parser()

    def get_all(self):
        return self.rules_data

    def get_available_rules(self):
        return [rule_data["rule"] for rule_data in self.rules_data]

    def get_rule(self, rule: str):
        for rule_data in self.rules_data:
            if rule_data.get("rule") == rule:
                return rule_data
