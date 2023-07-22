from typing import List
from dataclasses import dataclass, field
from src.rule_engine.action_data import ActionData


@dataclass
class ActionBuilder:
    actions: dict
    action_data: List[ActionData] = field(default_factory=list)

    def get_actions(self):
        for action in self.actions:
            self.action_data.append(ActionData(action["code"], action["destination"]))

