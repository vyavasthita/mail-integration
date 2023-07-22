from dataclasses import dataclass, field
from src.api_engine.api_request import ApiRequest
from src import env_configuration


@dataclass
class ApiEngine:
    api_request: ApiRequest = field(default_factory=ApiRequest)
    api_url: str = env_configuration.API_URL

    def move_message(self, api_data: tuple):
        # https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}/modify

        for data in api_data:
            request_body = {"addLabelIds": [data[1]], "removeLabelIds": []}

            url = f"{self.api_url}/users/me/messages/{data[0]}/modify"
            self.api_request.update_label(url=url, request_body=request_body)

    def read_unread_message(self, api_data: list):
        print("Read Unread")

        for data in api_data:
            print(data)
