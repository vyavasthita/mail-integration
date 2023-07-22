from src.auth_engine.api_auth import ApiAuth


class ApiRequest:
    def update_label(self, url: str, request_body: dict):
        with ApiAuth() as auth:
            auth.session.post(url, data=request_body)
