import jsonschema
from tests import settings as settings


class Endpoint:
    response = None
    response_json = None
    schema = {}
    url = settings.url
    headers = settings.headers
    expected_message = ""
    expected_error = "Требуется авторизация"

    def check_response_is_200(self):
        assert self.response.status_code == 200, \
            f'{self.response.status_code}'

    def check_response_is_201(self):
        assert self.response.status_code == 201, \
            f'{self.response.status_code}'

    def check_response_is_204(self):
        assert self.response.status_code == 204, \
            f'{self.response.status_code}'

    def check_response_is_401(self):
        assert self.response.status_code == 401, \
            f'{self.response.status_code}'

    def validate(self, data):
        jsonschema.validate(instance=data, schema=self.schema)

    def get_data(self):
        return self.response.json()

    def get_message(self):
        return self.get_data()["message"]

    def get_error(self):
        return self.get_data()["error"]

    def check_message(self):
        assert self.get_message() == self.expected_message, \
            f"Ответ API {self.get_message()} " \
            f"не совпадает с ожидаемым сообщением {self.expected_message}"

    def check_error(self):
        assert self.get_error() == self.expected_error, \
            f"Ответ API {self.get_error()} " \
            f"не совпадает с ожидаемой ошибкой {self.expected_error}"

    def get_user_id(self):
        return self.get_data()['user_id']

    def get_task_id(self):
        return self.get_data()['id']

    def get_task_title(self):
        return self.get_data()['title']

    def get_task_description(self):
        return self.get_data()['description']

    def get_task_status(self):
        return self.get_data()['completed']

    @staticmethod
    def check_task_in_db(cursor, task_data):
        cursor.execute(
            "SELECT * from task WHERE title =%s", (task_data['title'],)
        )
        added_task = cursor.fetchone()
        assert added_task is not None, "Задача не была найдена в базе данных"
        assert added_task[1] == task_data['title'], \
            (f"Имя задачи не совпадает. Ожидалось '{task_data['title']}',"
             f"но получено {added_task[1]}.")
        assert added_task[2] == task_data['description'], \
            (f"Описание задачи не совпадает."
             f"Ожидалось '{task_data['description']}',"
             f"но получено {added_task[2]}.")

    @staticmethod
    def check_task_not_exists(cursor, task_data):
        cursor.execute(
            'SELECT COUNT(*) from "user" WHERE username =%s',
            (task_data['title'],)
        )
        count = cursor.fetchone()[0]
        assert count == 0,\
            f"Задача c именем {task_data['title']} ,была добавлена в БД"