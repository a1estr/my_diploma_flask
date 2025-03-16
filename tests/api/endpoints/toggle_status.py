import requests
from tests.api.endpoints.base_endpoint import Endpoint


class ToggleStatus(Endpoint):
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

    def toggle_status(self, session, task_id):
        self.response = session.post(f'{self.url}/api/tasks/{task_id}/toggle')
        self.response_json = self.response.json()

    def toggle_status_non_auth(self, task_id):
        self.response = requests.post(f'{self.url}/api/tasks/{task_id}/toggle')
        self.response_json = self.response.json()

    @staticmethod
    def check_status_not_changed(cursor, task_data, status):
        cursor.execute(
            "SELECT * from task WHERE title =%s", (task_data['title'],)
        )
        task = cursor.fetchone()
        assert task[4] == status, \
            f"Статус задачи в базе данных {task[4]} был изменен на {status}"

