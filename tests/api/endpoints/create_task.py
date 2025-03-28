import requests
from tests.api.endpoints.base_endpoint import Endpoint


class CreateTask(Endpoint):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "integer"}
        },
        "required": [
            "id",
            "title",
            "description",
            "created_at",
            "completed",
            "user_id"
        ]
    }

    def create_task(self, task_data, session):
        self.response = session.post(f'{self.url}/api/tasks',
                                     json=task_data, headers=self.headers)
        self.response_json = self.response.json()

    def create_task_non_auth(self, task_data):
        self.response = requests.post(f'{self.url}/api/tasks',
                                      json=task_data, headers=self.headers)
        self.response_json = self.response.json()
