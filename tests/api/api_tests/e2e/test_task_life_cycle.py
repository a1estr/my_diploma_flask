from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.get_task import GetTask
from tests.api.data.user_data import valid_user_data
from tests.api.data.task_data import valid_task_data


def test_task_life_cycle(connect_to_db):
    # Зарегистрируем нового пользователя
    register_user = RegisterUser()
    register_user.register_user(valid_user_data)

    # Выполним проверки статуса запроса создания пользователя и валидации схемы
    register_user.check_response_is_201()
    register_user.validate(register_user.get_data())

    # Проверим получение сообщения об успешной регистрации пользователя
    register_user.check_message()

    # Авторизуемся созданным пользователем и инициируем сессию
    login = LoginUser()
    session = login.login_user(valid_user_data)

    # Выполним проверки статуса запроса аутентификации и валидации схемы
    login.check_response_is_200()
    login.validate(login.get_data())

    # Проверим получение сообщения об успешной аутентификации пользователя
    login.check_message()

    # Проверим username пользователя, который вернул сервер
    assert login.get_username() == valid_user_data['username'], (
        f"Username полученный от сервера {login.get_username()} != "
        f"{valid_user_data['username']}"
    )

    # Вернем id залогиненного пользователя
    user_id = login.get_user_id()

    # Создадим новую задачу
    create_task = CreateTask()
    create_task.create_task(valid_task_data, session)

    # Выполним проверки статуса запроса создания задачи и валидации схемы
    create_task.check_response_is_201()
    create_task.validate(create_task.get_data())

    # Получим ID созданной задачи
    task_id = create_task.get_task_id()

    # Получим созданную задачу по ID
    get_task = GetTask()
    get_task.get_task(task_id, session)

    # Проверим содержимое полученного ответа от сервера с данными по задаче
    assert get_task.get_task_title() == valid_task_data['title'], (
        f"Полученное имя задачи от сервера {get_task.get_task_title()}",
        f"не соответствует ожидаемому {valid_task_data['title']}")

    assert get_task.get_task_description() == valid_task_data['description'], (
        f"Полученное описание задачи от сервера {get_task.get_task_description()}",
        f"не соответствует ожидаемому {valid_task_data['description']}")

    assert get_task.get_task_description() == valid_task_data['description'], (
        f"Полученное описание задачи от сервера {get_task.get_task_description()}",
        f"не соответствует ожидаемому {valid_task_data['description']}")

    # Проверим, что задача принадлежит текущему пользователю
    assert get_task.get_user_id() == user_id, (
        f"Полученный ID пользователя {get_task.get_user_id()} из созданной задачи",
        f"не соответствует ожидаемому {user_id}")

    # Проверим, что задача была добавлена в базу данных
    create_task.check_task_in_db(connect_to_db)
