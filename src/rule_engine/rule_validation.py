import sys
from dataclasses import dataclass, field
from src.data_layer.mail_dao import MailDao
from src.utils.api_logger import ApiLogger
from src.rule_engine.rule_parser import RuleParser


@dataclass
class RuleValidation:
    rule_parser: RuleParser = field(default_factory=RuleParser)
    available_labels: list = field(default_factory=list)

    def set_available_labels(self):
        query = """SELECT label_id FROM label"""

        result_set = MailDao.read(query)

        for result in result_set:
            self.available_labels.append(result[0])

    def is_valid_labels(self, labels: dict):
        for rule, labels in labels.items():
            ApiLogger.log_info(f"Verifying labels for rule {rule}.")

            for label in labels:
                if label not in self.available_labels:
                    ApiLogger.log_error(
                        f"Invalid label '{label}' found for rule '{rule}' in rule parser. Available labels -> {self.available_labels}."
                    )
                    sys.exit(0)

    def verify_rules(self):
        # Verify labels
        self.set_available_labels()
        self.is_valid_labels(self.rule_parser.get_labels())
