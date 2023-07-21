from src.query_builder import AnyQueryBuilder, AllQueryBuilder


class RuleEngine:
    def __init__(self, rule: dict) -> None:
        self.rule = rule
        self.any_query_builder = AnyQueryBuilder()
        self.all_query_builder = AllQueryBuilder()

    def build(self):
        if self.rule["predicate"] == "all":
            return self.all_query_builder.build_all_predicate(self.rule["conditions"])
        elif self.rule["predicate"] == "any":
            return self.any_query_builder.build_any_predicate(self.rule["conditions"])
