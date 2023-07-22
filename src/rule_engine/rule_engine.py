from dataclasses import dataclass, field
from src.rule_engine.query_builder import AnyQueryBuilder, AllQueryBuilder
from src.rule_engine.action_builder import ActionBuilder
from src.utils.api_logger import ApiLogger
from src.data_layer.mail_dao import MailDao


@dataclass
class RuleEngine:
    rule_data: dict = field(default_factory=dict)

    def build_query(self, predicate: str, conditions: dict):
        if predicate == "all":
            all_query_builder = AllQueryBuilder()
            return all_query_builder.build_all_predicate(conditions)
        elif predicate == "any":
            any_query_builder = AnyQueryBuilder()
            return any_query_builder.build_any_predicate(conditions)

    def build_actions(self, actions: dict):
        action_builder = ActionBuilder(actions)

    def build(self, selected_rule_data: dict):
        query = self.build_query(
            selected_rule_data["predicate"], selected_rule_data["conditions"]
        )

        actions = self.build_actions(selected_rule_data["actions"])

        return query

    def start(self, selected_rule_data: dict):
        query = self.build(selected_rule_data)

        print(query)
