import requests
from tests.api.endpoints.base_endpoint import Endpoint


class UpdateTask(Endpoint):
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

    def update_task(self, session, task_id, task_data):
        self.response = session.put(
            f'{self.url}/api/tasks/{task_id}',
            json=task_data,
            headers=self.headers
        )
        self.response_json = self.response.json()

    def update_task_non_auth(self, task_id, task_data):
        self.response = requests.put(
            f'{self.url}/api/tasks/{task_id}',
            json=task_data,
            headers=self.headers
        )
        self.response_json = self.response.json()
