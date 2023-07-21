from src.query_builder import AnyQueryBuilder, AllQueryBuilder
from src.rule_data import RuleData
from utils.api_logger import ApiLogger


class RuleEngine:
    def __init__(self) -> None:
        self.rule_data = RuleData()
        self.any_query_builder = AnyQueryBuilder()
        self.all_query_builder = AllQueryBuilder()

    def build(self, selected_rule: str):
        selected_rule_data = self.rule_data.get_rule(selected_rule)

        predicate = selected_rule_data["predicate"]
        conditions = selected_rule_data["conditions"]

        if predicate == "all":
            return self.all_query_builder.build_all_predicate(conditions)
        elif predicate == "any":
            return self.any_query_builder.build_any_predicate(conditions)

    def apply_rule(self, selected_rule: str):
        ApiLogger.log_info(f"Applying rule {selected_rule}.")

        query = self.build(selected_rule)

        print(query)
