import requests
from tests.api.endpoints.base_endpoint import Endpoint


class DeleteTask(Endpoint):
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

    def delete_task(self, session, task_id):
        self.response = session.delete(f'{self.url}/api/tasks/{task_id}')

    def delete_task_non_auth(self, task_id):
        self.response = requests.delete(f'{self.url}/api/tasks/{task_id}')

    @staticmethod
    def check_task_deleted_from_db(cursor, task_id):
        cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        assert task is None, \
            f"Задача с ID {task_id} не была удалена из базы данных"
