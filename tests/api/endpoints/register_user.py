import requests
from tests.api.endpoints.base_endpoint import Endpoint


class RegisterUser(Endpoint):
    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }
    expected_message = "Регистрация успешна"

    def register_user(self, user_data):
        self.response = requests.post(f'{self.url}/api/register',
                                      json=user_data, headers=self.headers)
        self.response_json = self.response.json()

    @staticmethod
    def user_not_exists(cursor, username):
        cursor.execute(
            'SELECT COUNT(*) from "user" WHERE username =%s',
            (username,)
        )
        count = cursor.fetchone()[0]
        return count == 0
