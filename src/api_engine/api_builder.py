from dataclasses import dataclass
from src import env_configuration


@dataclass
class ApiBuilder:
    api_url: str = env_configuration.API_URL

    def get_modify_api_url(self, id: str, user_id: str, request_body):
        # https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}/modify

        return f"{self.api_url}/users/{user_id}/messages/{id}/modify"
