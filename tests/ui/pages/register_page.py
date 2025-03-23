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

    def valid_register(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_register()

    @staticmethod
    def user_not_exists(cursor, username):
        cursor.execute(
            'SELECT COUNT(*) from "user" WHERE username =%s',
            (username,)
        )
        count = cursor.fetchone()[0]
        return count == 0