from dataclasses import dataclass


@dataclass
class ActionBuilder:
    actions: dict

    def get_action(self):
        for action in self.actions:
            pass