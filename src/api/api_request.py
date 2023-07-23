"""To make api requests to gmail rest api.

@file api_request.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This modules talks to gmail rest api.
    It marks messages read/unread or can move messages to another label.
"""
# Core python packages
from typing import List
from dataclasses import dataclass

# Application packages
from src import env_configuration
from src.rule_engine.action_data import ActionData, ActionCode
from src.auth.connection import AuthConnection


@dataclass
class ApiRequest:
    api_url: str = env_configuration.API_URL

    def get_labels(self, action_data: List[ActionData]) -> tuple:
        """
        From rule parse dict object, we write labels to list.
        This is request because gmail api expects labels as list.

        Args:
            action_data (List[ActionData]): Labels from rule parser.

        Returns:
            tuple: Labels to be added and removed
        """
        add_labels = list()
        remove_labels = list()

        for data in action_data:
            if data.code in [ActionCode.MOVE, ActionCode.UNREAD]:
                add_labels.append(data.label)
            else:
                remove_labels.append("UNREAD")

        return add_labels, remove_labels

    def gen_request_body(self, message_ids: list, action_data: List[ActionData]) -> dict:
        """
        Generate Request body for calling gmail rest api.

        Args:
            message_ids (list): Messages for which update is required.
            action_data (List[ActionData]): Rule parser data which will be sent as list
            to gmail rest api.

        Returns:
            dict: Request body as dict
        """
        ids = [message_id[0] for message_id in message_ids]
        add_labels, remove_labels = self.get_labels(action_data)
        return {"ids": ids, "addLabelIds": add_labels, "removeLabelIds": remove_labels}

    def update_label(self, message_ids: list, action_data: List[ActionData]) -> None:
        """
        Call Rest api to update label of messages.
        Request is sent as batch.

        Args:
            message_ids (list): Messages for which update is required.
            action_data (List[ActionData]): Rule parser data which will be sent as list
        """
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/batchModify"

        with AuthConnection() as auth:
            auth.session.post(url, data=self.gen_request_body(message_ids, action_data))
