import jsonschema
import tests.api.settings as settings


class Endpoint:
    response = None
    response_json = None
    schema = {}
    url = settings.url
    headers = settings.headers
    expected_message = ""

    def check_response_is_200(self):
        assert self.response.status_code == 200,\
            f'{self.response.status_code}'

    def check_response_is_201(self):
        assert self.response.status_code == 201,\
            f'{self.response.status_code}'

    def check_response_is_400(self):
        assert self.response.status_code == 400,\
            f'{self.response.status_code}'

    def validate(self, data):
        jsonschema.validate(instance=data, schema=self.schema)

    def get_data(self):
        return self.response.json()

    def get_message(self):
        return self.get_data()["message"]

    def check_message(self):
        assert self.get_message() == self.expected_message,\
            f"Ответ API {self.get_message()} "\
            f"не совпадает с ожидаемым сообщением {self.expected_message}"

    def get_user_id(self):
        return self.get_data()['user_id']
