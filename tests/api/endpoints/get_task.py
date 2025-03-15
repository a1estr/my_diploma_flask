import requests
from dateutil.parser import isoparse
from tests.api.endpoints.base_endpoint import Endpoint


class GetTask(Endpoint):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "description": {"type": "integer"},
            "created_at": {"type": "string"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "integer"}

        },
        "required": ["id", "description", "created_at", "completed", "user_id"]
    }

    def get_task(self, task_id, session):
        self.response = session.get(f'{self.url}/api/tasks/{task_id}')
        self.response_json = self.response.json()

    def get_task_id(self):
        return self.get_data()['id']

    def get_task_title(self):
        return self.get_data()['title']

    def get_task_description(self):
        return self.get_data()['description']

    def get_create_time(self):
        create_time = self.get_data()['created_at']
        dt = isoparse(create_time)
        return dt.replace(microsecond=0).isoformat()