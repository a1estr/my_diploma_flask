from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage
from tests.settings import url


class RegisterPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-testid="username-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="password-input"]')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[data-testid="register-button"]')
    LOGIN_LINK = (By.CSS_SELECTOR, '[data-testid="login-link"]')
    REGISTER_MESSAGE = (By.CSS_SELECTOR, '[data-testid="flash-message-success"]')

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_register(self):
        self.click_element(self.REGISTER_BUTTON)

    def get_register_message(self):
        return self.find_element(self.REGISTER_MESSAGE).text

    def get_register_page(self):
        return self.open_url(f"{url}register")

    def go_to_login_page(self):
        self.click_element(self.LOGIN_LINK)

    @staticmethod
    def check_user_in_db(cursor, username):
            cursor.execute(
                'SELECT * from "user" WHERE username =%s', (username,)
            )
            created_user = cursor.fetchone()
            assert created_user is not None, "Пользователь не был найден в БД"
            assert created_user[1] == username, \
                (f"Username не совпадает. Ожидалось '{username}',"
             f"но получено {created_user[1]}.")