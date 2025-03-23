import allure
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.register_page import RegisterPage
from tests.ui.pages.tasks_page import TasksPage


@allure.feature("Пользователи")
@allure.story("Регистрация и авторизация")
@allure.title("Регистрация нового пользователя и вход в систему")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("UI", "Registration", "Authorization", "Users")
def test_register_and_login(driver, connect_to_db, unique_user_data):
    """
    Тест проверяет процесс регистрации и входа в систему
    """
    # Сгенерируем уникальные данные пользователя
    with allure.step("Генерация тестовых данных"):
        username, password = unique_user_data
        allure.attach(
            f"Сгенерированное имя пользователя: {username}\n"
            f"Сгенерированный пароль: {password}",
            name="Generated userdata"
        )

    # Перейдем на страницу входа в систему
    with allure.step("Переход на страницу авторизации"):
        login_page = LoginPage(driver)
        login_page.get_login_page()
        login_page.attach_screenshot(
            login_page.LOGIN_BUTTON,
            "Opened login page"
        )

    # Перейдем на страницу регистрации пользователя
    with allure.step("Переход на страницу регистрации"):
        login_page.go_to_register_page()
        register_page = RegisterPage(driver)
        register_page.attach_screenshot(
            register_page.REGISTER_BUTTON,
            "Opened register page"
        )
        assert "register" in driver.current_url, \
            "Перенаправление на страницу регистрации не произошло"

    # Зарегистрируем нового пользователя с уникальными данными
    with (allure.step("Регистрация нового пользователя")):
        with allure.step("Заполнение имени пользователя и пароля"):
            register_page.enter_username(username)
            register_page.enter_password(password)
            register_page.attach_screenshot(
                register_page.REGISTER_BUTTON,
                "Register page before click Register button"
            )
            register_page.click_register()

        register_page.attach_screenshot(
            register_page.REGISTER_MESSAGE,
            "Completed Registration"
        )

        # Проверим, что сообщение об успешной регистрации появилось
        with allure.step("Сообщение об успешной регистрации"):
            register_message = register_page.get_register_message()
            success_register_message = ("Регистрация успешна!"
                                        " Теперь вы можете войти")
            assert register_message == success_register_message, (
                f"Неверный текст сообщения:\n {register_message}\n",
                f"Ожидалось:\n {success_register_message}"
            )

        # Проверим, что мы перешли на страницу логина
        with allure.step("Редирект на страницу логина"):
            assert "login" in driver.current_url, \
                "Перенаправление на страницу входа в систему не произошло"

        # Проверим, что пользователь появился в базе данных
        with allure.step("Наличие пользователя в базе данных"):
            login_page.check_user_in_db(connect_to_db, username)

    # Авторизуемся в системе
    with allure.step("Авторизация пользователя"):
        with allure.step("Заполнение имени пользователя и пароля"):
            login_page.enter_username(username)
            login_page.enter_password(password)
            login_page.attach_screenshot(
                login_page.LOGIN_BUTTON,
                "Login page before click Login button"
            )
            login_page.click_login()

        tasks_page = TasksPage(driver)
        tasks_page.attach_screenshot(
            tasks_page.FLASH_MESSAGE_SUCCESS,
            "Tasks page"
        )

        # Проверим, что мы перешли на страницу задач
        with allure.step("Редирект на страницу задач"):
            assert "tasks" in driver.current_url, \
                "Перенаправление на страницу с задачами не произошло"

        # Проверим, что авторизация прошла успешно
        with allure.step("Cообщение об успешном входе"):
            tasks_message = tasks_page.get_flash_success_message()
            expected_tasks_message = "Вы успешно вошли в систему"
            assert tasks_message == expected_tasks_message, (
                f"Неверный текст сообщения:\n {tasks_message}\n",
                f"Ожидалось:\n {expected_tasks_message}"
            )

        # Проверим корректность отображения имени пользователя в кнопке "Выйти"
        with allure.step("Отображение имени пользователя в кнопке 'Выйти'"):
            logout_button_text = tasks_page.get_logout_button_text()
            expected_logout_button_text = f"Выйти ({username})"
            assert logout_button_text == expected_logout_button_text, (
                f"Некорректный текст кнопки 'Выйти':\n {logout_button_text}\n",
                f"Ожидалось:\n {expected_logout_button_text}"
            )

    # Выйдем из системы
    with allure.step("Выход из системы"):
        tasks_page.click_logout_button()
        login_page.attach_screenshot(
            login_page.INFO_MESSAGE,
            "Login Page after Logout"
        )

        with allure.step(
                "Редирект на страницу логина после выхода из системы"
        ):
            assert "login" in driver.current_url, \
                "Перенаправление на страницу входа в систему не произошло"

        # Проверка получения сообщения об успешном выходе из системы
        with allure.step("Сообщение об успешном выходе"):
            logout_message = login_page.get_info_message()
            expected_logout_message = "Вы вышли из системы"
            assert logout_message == expected_logout_message, (
                f"Неверный текст сообщения:\n {logout_message}\n",
                f"Ожидалось:\n {expected_logout_message}"
            )
