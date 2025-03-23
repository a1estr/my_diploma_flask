import allure
import pytest
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.get_task import GetTask
from tests.api.endpoints.update_task import UpdateTask
from tests.api.endpoints.toggle_status import ToggleStatus
from tests.api.endpoints.delete_task import DeleteTask
from tests.data.user_data import valid_user_data1, valid_user_data2
from tests.data.task_data import (valid_task_data1,
                                  valid_task_data2,
                                  valid_updated_task_data1,
                                  valid_updated_task_data2)


@pytest.mark.parametrize(
    "user_data, task_data, updated_task_data",
    [
        (valid_user_data1, valid_task_data1, valid_updated_task_data1),
        (valid_user_data2, valid_task_data1, valid_updated_task_data1),
        (valid_user_data1, valid_task_data2, valid_updated_task_data1),
        (valid_user_data2, valid_task_data2, valid_updated_task_data2)
    ]
)
@allure.feature("Задачи (Tasks)")
@allure.story("Полный жизненный цикл задачи")
@allure.title("Проверка полного жизненного цикла задачи через API")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("API", "Smoke", "CRUD", "Tasks")
def test_task_life_cycle(connect_to_db, user_data,
                         task_data, updated_task_data):
    """
    Тест проверяет полный жизненный цикл задачи через API
    """
    # Зарегистрируем нового пользователя, если его еще нет
    register = RegisterUser()
    if register.user_not_exists(connect_to_db, user_data['username']):
        with allure.step("Регистрация нового пользователя"):
            with allure.step("Отправка запроса на регистрацию"):
                register.register_user(user_data)
                allure.attach(
                    str(user_data),
                    name="Register Request Data",
                    attachment_type=allure.attachment_type.JSON
                )

            # Выполним проверки статуса запроса
            # создания пользователя и валидации схемы
            with allure.step("Проверка статуса ответа и валидации схемы"):
                response_data = register.get_data()
                allure.attach(
                    str(response_data),
                    name="Register Response Data",
                    attachment_type=allure.attachment_type.JSON
                )
                register.check_response_is_201()
                register.validate(register.get_data())

            # Проверим получение сообщения об успешной регистрации пользователя
            with allure.step("Проверка сообщения о регистрации"):
                register.check_message()

    # Авторизуемся созданным пользователем и инициируем сессию
    with allure.step("Авторизация пользователя"):
        login = LoginUser()
        with allure.step("Отправка запроса на авторизацию пользователя"):
            session = login.login_user(user_data)
            allure.attach(
                str(user_data),
                name="Login Request Data",
                attachment_type=allure.attachment_type.JSON
            )

        # Выполним проверки статуса запроса авторизации и валидации схемы
        with allure.step("Проверка статуса ответа и валидации схемы"):
            login.check_response_is_200()
            login.validate(login.get_data())
            allure.attach(
                str(login.get_data()),
                name="Login Response Data",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверим получение сообщения об успешной аутентификации пользователя
        with allure.step("Проверка сообщения об успешной аутентификации"):
            login.check_message()

        # Проверим username пользователя, который вернул сервер
        with allure.step("Проверка username пользователя из ответа"):
            expected_username = user_data['username']
            actual_username = login.get_username()
            allure.attach(
                f"Ожидаемый username: {expected_username}\n"
                f"Фактический: {actual_username}",
                name="Username Comparison"
            )
            assert actual_username == expected_username, \
                (f"Несоответствие usernames:"
                 f"{actual_username} != {expected_username}")

    # Вернем id залогиненного пользователя
    user_id = login.get_user_id()

    # Создадим новую задачу
    with allure.step("Создание новой задачи"):
        create_task = CreateTask()
        with allure.step("Отправка запроса на создание задачи"):
            create_task.create_task(task_data, session)
            allure.attach(
                str(task_data),
                name="Task Creation Request Data",
                attachment_type=allure.attachment_type.JSON
            )

        # Выполним проверки статуса запроса создания задачи и валидации схемы
        with allure.step("Проверка статуса ответа и валидации схемы"):
            create_task.check_response_is_201()
            create_task.validate(create_task.get_data())
            allure.attach(
                str(create_task.get_data()),
                name="Task Created Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверим, что задача была добавлена в базу данных и сверим содержимое
        with allure.step("Проверка, что задача добавлена в БД"):
            create_task.check_task_in_db(connect_to_db, task_data)

    # Получим ID созданной задачи
    task_id = create_task.get_task_id()

    # Получим созданную задачу по ID
    with allure.step("Получение созданной задачи по ID"):
        get_task = GetTask()
        with allure.step("Отправка запроса на получение задачи по ID"):
            get_task.get_task(task_id, session)

        # Выполним проверки статуса запроса задачи по ID и валидации схемы
        with allure.step("Проверка статуса ответа и валидации схемы"):
            get_task.check_response_is_200()
            get_task.validate(get_task.get_data())
            allure.attach(
                str(get_task.get_data()),
                name="Get Task Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверим содержимое полученного ответа от сервера с данными по задаче
        with allure.step("Проверка содержимого задачи"):
            allure.attach(
                f"Ожидаемое имя задачи: {task_data['title']} \n"
                f"Фактическое имя задачи: {get_task.get_task_title()}",
                name="Title Comparison"
            )
            assert get_task.get_task_title() == task_data['title'], (
                f"Полученное имя задачи от сервера"
                f"{get_task.get_task_title()}",
                f"не соответствует ожидаемому"
                f"{task_data['title']}")

            allure.attach(
                f"Ожидаемое описание задачи:"
                f"{task_data['description']} \n"
                f"Фактическое описание задачи:"
                f"{get_task.get_task_description()}",
                name="Description Comparison"
            )
            assert get_task.get_task_description() == task_data[
                'description'
            ], (
                f"Полученное описание задачи от сервера"
                f"{get_task.get_task_description()}",
                f"не соответствует ожидаемому"
                f"{task_data['description']}"
            )

            allure.attach(
                f"Ожидаемый user ID у задачи: {user_id} \n"
                f"Фактический user ID у задачи: {get_task.get_user_id()}",
                name="User ID Comparison"
            )
            # Проверим, что задача принадлежит текущему пользователю
            assert get_task.get_user_id() == user_id, (
                f"Полученный ID пользователя {get_task.get_user_id()}",
                f"не соответствует ожидаемому {user_id}")

    # Изменим название, описание задачи и переведем ее в выполненную
    with allure.step("Обновление задачи"):
        update_task = UpdateTask()
        with allure.step("Отправка запроса на обновление задачи"):
            update_task.update_task(session, task_id, updated_task_data)
            allure.attach(
                str(updated_task_data),
                name="Update Request Data",
                attachment_type=allure.attachment_type.JSON
            )

        # Выполним проверки статуса запроса обновления задачи и валидации схемы
        with allure.step("Проверка статуса ответа и валидации схемы"):
            update_task.check_response_is_200()
            update_task.validate(update_task.get_data())
            allure.attach(
                str(update_task.get_data()),
                name="Update Task Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверим содержимое полученного ответа от сервера
        # с обновленными данными по задаче
        with allure.step("Проверка обновленных данных задачи"):
            allure.attach(
                f"Ожидаемое имя задачи: {updated_task_data['title']} \n"
                f"Фактическое имя задачи: {update_task.get_task_title()}",
                name="Title Comparison"
            )
            assert update_task.get_task_title() == updated_task_data[
                'title'
            ], (
                f"Полученное имя задачи от сервера"
                f"{update_task.get_task_title()}",
                f"не соответствует ожидаемому"
                f"{updated_task_data['title']}"
            )

            allure.attach(
                f"Ожидаемое описание задачи:\n"
                f"{updated_task_data['description']} \n"
                f"Фактическое описание задачи:\n"
                f"{update_task.get_task_description()}",
                name="Description Comparison"
            )
            assert update_task.get_task_description() == updated_task_data[
                'description'
            ], (
                f"Полученное описание задачи от сервера"
                f"{update_task.get_task_description()}",
                f"не соответствует ожидаемому"
                f"{updated_task_data['description']}"
            )

            if 'completed' in updated_task_data.keys():
                allure.attach(
                    f"Ожидаемый статус задачи:"
                    f"{updated_task_data['completed']} \n"
                    f"Фактический статус задачи:"
                    f"{update_task.get_task_status()}",
                    name="Status Comparison"
                )
                assert update_task.get_task_status() == updated_task_data[
                    'completed'
                ], (
                    f"Полученный статус задачи"
                    f"{update_task.get_task_status()}",
                    f"не соответствует ожидаемому"
                    f"{updated_task_data['completed']}"
                )

        # Проверим, что данные задачи изменились в бд
        with allure.step("Проверка, что задача изменилась в БД"):
            update_task.check_task_in_db(connect_to_db, updated_task_data)

    # Изменим статус задачи
    with allure.step("Изменение статуса задачи"):
        task_status = ToggleStatus()
        task_status.toggle_status(session, task_id)

        # Проверим статус запроса изменения задачи и валидации схемы
        with allure.step("Проверка статуса ответа и валидации схемы"):
            task_status.check_response_is_200()
            task_status.validate(task_status.get_data())
            allure.attach(
                str(task_status.get_data()),
                name="Update Task Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверим, что статус изменился
        with allure.step("Проверка изменения статуса"):
            new_status = task_status.get_task_status()
            previous_status = update_task.get_task_status()
            allure.attach(
                f"Новый статус задачи: {new_status} \n"
                f"Предыдущий статус задачи: {previous_status}",
                name="Status Comparison"
            )
            assert new_status is not previous_status, \
                "Статус задачи не изменился"

    # Удалим задачу
    with allure.step("Удаление задачи"):
        delete_task = DeleteTask()
        delete_task.delete_task(session, task_id)

        # Проверим статус запроса удаления задачи
        with allure.step("Проверка статуса ответа"):
            delete_task.check_response_is_204()

        # Проверим, что задача была удалена
        with allure.step("Проверка удаления задачи из БД"):
            delete_task.check_task_deleted_from_db(connect_to_db, task_id)
