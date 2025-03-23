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
from tests.settings import db_params
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.data.user_data import valid_user_data1
from tests.data.task_data import valid_task_data1
from tests.api.endpoints.delete_task import DeleteTask
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.register_page import RegisterPage


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
def unique_user_data():
    """
    Фикстура для генерации уникальных данных пользователя
    """
    fake = Faker()
    username = fake.user_name()
    password = fake.password(length=6)
    return username, password


@pytest.fixture(params=["Chrome", "Firefox"])
def driver(request):
    """
    Фикстура для запуска тестов в двух браузерах
    (Chrome и Firefox)
    """
    browser = request.param
    config_driver = None

    if browser == "Chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--disable-gpu')
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = '/usr/bin/google-chrome-stable'
        service = ChromeService('/usr/local/bin/chromedriver')
        config_driver = webdriver.Chrome(service=service, options=options)

    elif browser == "Firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = '/usr/bin/firefox'
        service = FirefoxService(GeckoDriverManager().install())
        config_driver = webdriver.Firefox(service=service, options=options)

    yield config_driver
    config_driver.quit()


@pytest.fixture
def driver_login(driver, connect_to_db):
    """
    Фикстура для предварительной регистрации пользователя
    и авторизации в системе
    """

    # Регистрация пользователя, если его нет в бд
    register_page = RegisterPage(driver)
    username, password = valid_user_data1['username'], valid_user_data1["password"]
    if register_page.user_not_exists(connect_to_db, username):
        register_page.get_register_page()
        register_page.valid_register(username, password)

    # Вход в систему
    login_page = LoginPage(driver)
    login_page.valid_login(username, password)
    return driver
