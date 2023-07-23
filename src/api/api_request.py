from typing import List
from dataclasses import dataclass
from src import env_configuration
from src.rule_engine.action_data import ActionData, ActionCode
from src.auth.connection import AuthConnection


@dataclass
class ApiRequest:
    api_url: str = env_configuration.API_URL

    def get_message_ids(self, message_ids: list):
        return [message_id[0] for message_id in message_ids]

    def get_labels(self, action_data: List[ActionData]):
        add_labels = list()
        remove_labels = list()

        for data in action_data:
            if data.code in [ActionCode.MOVE, ActionCode.UNREAD]:
                add_labels.append(data.label)
            else:
                remove_labels.append("UNREAD")

        return add_labels, remove_labels

    def get_request_body(self, message_ids: list, action_data: List[ActionData]):
        ids = self.get_message_ids(message_ids)
        add_labels, remove_labels = self.get_labels(action_data)
        print("******#############################*********")
        print({"ids": ids, "addLabelIds": add_labels, "removeLabelIds": remove_labels})
        print("******#############################*********")
        return {"ids": ids, "addLabelIds": add_labels, "removeLabelIds": remove_labels}

    def update_label(self, message_ids: list, action_data: List[ActionData]):
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/batchModify"

        with AuthConnection() as auth:
            auth.session.post(url, data=self.get_request_body(message_ids, action_data))
