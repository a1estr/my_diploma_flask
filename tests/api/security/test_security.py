import allure
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.get_task import GetTask
from tests.api.endpoints.update_task import UpdateTask
from tests.api.endpoints.toggle_status import ToggleStatus
from tests.api.endpoints.delete_task import DeleteTask
from tests.api.data.task_data import valid_task_data1, valid_updated_task_data1


@allure.feature('Безопасность API')
@allure.story('Создание задачи')
@allure.title('Создание задачи без авторизации')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "Security", "Create")
def test_security_create_task(connect_to_db):
    # Попытаемся создать задачу без авторизации
    with allure.step('Попытка создать задачу без авторизации'):
        create_task = CreateTask()
        create_task.create_task_non_auth(valid_task_data1)
        allure.attach(
            str(create_task.get_data()),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    # Проверим полученный статус код
    with allure.step('Проверка полученного статус кода (401)'):
        create_task.check_response_is_401()

    # Проверим корректность сообщения об ошибке авторизации
    with allure.step('Проверка корректности сообщения об ошибке авторизации'):
        create_task.check_error()

    # Убедимся, что задача не была добавлена в бд
    with allure.step('Проверка, что задача не была добавлена в БД'):
        create_task.check_task_not_exists(connect_to_db, valid_task_data1)


@allure.feature('Безопасность API')
@allure.story('Обновление задачи')
@allure.title('Обновление задачи без авторизации')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "Security", "Update")
def test_security_update_task(connect_to_db, created_task):
    # Получим ID уже созданной задачи в БД
    task_id = created_task[0]

    # Попытаемся обновить задачу без авторизации
    with allure.step(f'Попытка обновить задачу с ID {task_id} без авторизации'):
        update_task = UpdateTask()
        update_task.update_task_non_auth(task_id, valid_updated_task_data1)
        allure.attach(
            str(update_task.get_data()),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    # Проверим полученный статус код
    with allure.step('Проверка полученного статус кода (401)'):
        update_task.check_response_is_401()

    # Проверим корректность сообщения об ошибке авторизации
    with allure.step('Проверка корректности сообщения об ошибке авторизации'):
        update_task.check_error()

    # Убедимся, что задача не была изменена в бд
    with allure.step('Проверка, что задача не была изменена в БД'):
        update_task.check_task_in_db(connect_to_db, valid_task_data1)


@allure.feature('Безопасность API')
@allure.story('Получение задачи по ID')
@allure.title('Получение задачи по ID без авторизации')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "Security", "Get")
def test_security_get_task(created_task):
    # Получим ID уже созданной задачи в БД
    task_id = created_task[0]

    # Попытаемся получить задачу по ID без авторизации
    with allure.step(f'Попытка получить задачу с ID {task_id} без авторизации'):
        get_task = GetTask()
        get_task.get_task_non_auth(task_id)
        allure.attach(
            str(get_task.get_data()),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    # Проверим полученный статус код
    with allure.step('Проверка полученного статус кода (401)'):
        get_task.check_response_is_401()

    # Проверим корректность сообщения об ошибке авторизации
    with allure.step('Проверка корректности сообщения об ошибке авторизации'):
        get_task.check_error()


@allure.feature('Безопасность API')
@allure.story('Изменение статуса задачи')
@allure.title('Изменение статуса задачи без авторизации')
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("API", "Security", "Status")
def test_security_toggle_status(connect_to_db, created_task):
    # Получим ID уже созданной задачи в БД
    task_id, completed = created_task

    # Попытаемся изменить статус задачи без авторизации
    with allure.step(f'Попытка изменить статус задачи с ID {task_id} без авторизации'):
        task_status = ToggleStatus()
        task_status.toggle_status_non_auth(task_id)
        allure.attach(
            str(task_status.get_data()),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    # Проверим полученный статус код
    with allure.step('Проверка полученного статус кода (401)'):
        task_status.check_response_is_401()

    # Проверим корректность сообщения об ошибке авторизации
    with allure.step('Проверка корректности сообщения об ошибке авторизации'):
        task_status.check_error()

    # Убедимся, что статус задачи не был изменен в бд
    with allure.step('Проверка, что статус задачи не был изменен в БД'):
        task_status.check_status_not_changed(connect_to_db, valid_task_data1, completed)


@allure.feature('Безопасность API')
@allure.story('Удаление задачи')
@allure.title('Удаление задачи без авторизации')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "Security", "Delete")
def test_security_delete_task(connect_to_db, created_task):
    # Получим ID уже созданной задачи в БД
    task_id = created_task[0]

    # Попытаемся удалить задачу без авторизации
    with allure.step(f'Попытка удалить задачу с ID {task_id} без авторизации'):
        delete_task = DeleteTask()
        delete_task.delete_task_non_auth(task_id)
        allure.attach(
            str(delete_task.get_data()),
            name="Response Data",
            attachment_type=allure.attachment_type.JSON
        )

    # Проверим полученный статус код
    with allure.step('Проверка полученного статус кода (401)'):
        delete_task.check_response_is_401()

    # Проверим корректность сообщения об ошибке авторизации
    with allure.step('Проверка корректности сообщения об ошибке авторизации'):
        delete_task.check_error()

    # Убедимся, что задача не была удалена из БД
    with allure.step('Проверка, что задача не была удалена из БД'):
        delete_task.check_task_in_db(connect_to_db, valid_task_data1)
