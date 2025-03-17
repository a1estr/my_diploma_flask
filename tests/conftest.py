import pytest
import psycopg2
from selenium import webdriver
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
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


@pytest.fixture
def chrom_driver():
    """
    Фикстура для настройки Chrome WEB-драйвера
    """
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    config_driver = webdriver.Chrome(service=service, options=options)
    yield config_driver
    config_driver.quit()


@pytest.fixture
def unique_user_data():
    """
    Фикстура для генерации уникальных данных пользователя
    """
    fake = Faker()
    username = fake.user_name()
    password = fake.password(length=6)
    return username, password


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """
    Фикстура для запуска тестов в двух браузерах
    (Chrome и Firefox)
    """
    browser = request.param
    config_driver = None

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        service = ChromeService(ChromeDriverManager().install())
        config_driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        service = FirefoxService(GeckoDriverManager().install())
        config_driver = webdriver.Firefox(service=service, options=options)

    yield config_driver
    config_driver.quit()
