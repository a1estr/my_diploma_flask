import requests
from tests.api.endpoints.base_endpoint import Endpoint


class LoginUser(Endpoint):
    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "user_id": {"type": "integer"},
            "username": {"type": "string"}

        },
        "required": ["message", "user_id", "username"]
    }
    expected_message = "Вы успешно вошли в систему"

    def login_user(self, user_data):
        session = requests.Session()
        self.response = session.post(
            f'{self.url}/api/login',
            json=user_data,
            headers=self.headers
        )
        self.response_json = self.response.json()
        return session

    def get_username(self):
        return self.get_data()['username']
