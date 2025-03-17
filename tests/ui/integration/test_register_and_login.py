from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.register_page import RegisterPage
from tests.ui.pages.tasks_page import TasksPage


def test_register_and_login(driver, connect_to_db, unique_user_data):
    # Сгенерируем уникальные данные пользователя
    username, password = unique_user_data

    # Перейдем на страницу входа в систему
    login_page = LoginPage(driver)
    login_page.get_login_page()

    # Перейдем на страницу регистрации пользователя
    login_page.go_to_register_page()
    register_page = RegisterPage(driver)

    # Зарегистрируем нового пользователя с уникальными данными
    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.click_register()

    # Проверим, что сообщение об успешной регистрации появилось
    register_message = register_page.get_register_message()
    success_register_message = "Регистрация успешна! Теперь вы можете войти"
    assert register_message == success_register_message, (
        f"Неверный текст сообщения:\n {register_message}\n",
        f"Ожидалось:\n {success_register_message}"
    )

    # Проверим, что мы перешли на страницу логина
    assert "login" in driver.current_url, \
        "Перенаправление на страницу входа в систему не произошло"

    # Проверим, что пользователь появился в базе данных
    register_page.check_user_in_db(connect_to_db, username)

    # Авторизуемся в системе
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Проверим, что мы перешли на страницу задач
    assert "tasks" in driver.current_url, \
        "Перенаправление на страницу с задачами не произошло"

    # Проверим, что авторизация прошла успешно
    tasks_page = TasksPage(driver)
    tasks_message = tasks_page.get_flash_success_message()
    expected_tasks_message = "Вы успешно вошли в систему"
    assert tasks_message == expected_tasks_message, (
        f"Неверный текст сообщения:\n {tasks_message}\n",
        f"Ожидалось:\n {expected_tasks_message}"
    )

    # Проверим корректность отображения имени пользователя в кнопке "Выйти"
    logout_button_text = tasks_page.get_logout_button_text()
    expected_logout_button_text = f"Выйти ({username})"
    assert logout_button_text == expected_logout_button_text, (
        f"Некорректный текст кнопки 'Выйти':\n {logout_button_text}\n",
        f"Ожидалось:\n {expected_logout_button_text}"
    )

    # Выйдем из системы
    tasks_page.click_logout_button()

    # Проверка перенаправления на страницу входа в систему
    assert "login" in driver.current_url, \
        "Перенаправление на страницу входа в систему не произошло"

    # Проверка получения сообщения об успешном выходе из системы
    logout_message = login_page.get_info_message()
    expected_logout_message = "Вы вышли из системы"
    assert logout_message == expected_logout_message, (
        f"Неверный текст сообщения:\n {logout_message}\n",
        f"Ожидалось:\n {expected_logout_message}"
    )
