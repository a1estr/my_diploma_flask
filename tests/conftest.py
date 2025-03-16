import pytest
import psycopg2
from settings import db_params
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.data.user_data import valid_user_data1
from tests.api.data.task_data import valid_task_data1
from tests.api.endpoints.delete_task import DeleteTask


@pytest.fixture
def connect_to_db():
    """
    Фикстура подключения к базе данных
    """
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()


@pytest.fixture
def created_task(connect_to_db):
    """
    Фикстура для создания задачи для API тестов
    """
    register = RegisterUser()
    if register.user_not_exists(connect_to_db, valid_user_data1['username']):
        register.register_user(valid_user_data1)
    login = LoginUser()
    session = login.login_user(valid_user_data1)
    create_task = CreateTask()
    create_task.create_task(valid_task_data1, session)
    task_id = create_task.get_task_id()
    task_status = create_task.get_task_status()
    yield task_id, task_status
    delete_task = DeleteTask()
    delete_task.delete_task(session, task_id)
