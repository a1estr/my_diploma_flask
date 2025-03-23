import requests
from tests.api.endpoints.base_endpoint import Endpoint


class GetTask(Endpoint):
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

    def get_task(self, task_id, session):
        self.response = session.get(f'{self.url}/api/tasks/{task_id}')
        self.response_json = self.response.json()

    def get_task_non_auth(self, task_id):
        self.response = requests.get(f'{self.url}/api/tasks/{task_id}')
        self.response_json = self.response.json()
