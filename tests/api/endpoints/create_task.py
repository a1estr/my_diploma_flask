import requests
import psycopg2
from tests.api.endpoints.base_endpoint import Endpoint
from tests.api.settings import db_params


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
        "required": ["id", "title", "description", "created_at", "completed", "user_id"]
    }

    def create_task(self, task_data, session):
        self.response = session.post(f'{self.url}/api/tasks',
                                      json=task_data, headers=self.headers)
        self.response_json = self.response.json()

    def get_task_id(self):
        return self.get_data()['id']

    def get_task_title(self):
        return self.get_data()['title']

    def get_task_description(self):
        return self.get_data()['description']

    def check_task_in_db(self, cursor):
        cursor.execute("SELECT * from task WHERE title =%s", (self.get_task_title(),))
        added_task = cursor.fetchone()
        assert added_task is not None, "Задача не была добавлена в базу данных!"
        assert added_task[1] == self.get_task_title(), \
            f"Имя задачи не совпадает. Ожидалось '{self.get_task_title()}', но получено {added_task[1]}."
