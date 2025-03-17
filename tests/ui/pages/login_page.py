from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage
from tests.settings import url


class LoginPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-testid="username-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="password-input"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-button"]')
    REGISTER_LINK = (By.CSS_SELECTOR, '[data-testid="register-link"]')
    INFO_MESSAGE = (By.CSS_SELECTOR, '[data-testid="flash-message-info"]')

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def get_info_message(self):
        return self.find_element(self.INFO_MESSAGE).text

    def get_login_page(self):
        return self.open_url(f"{url}login")

    def go_to_register_page(self):
        self.click_element(self.REGISTER_LINK)

    def valid_login(self, name, password):
        self.get_login_page()
        self.enter_username(name)
        self.enter_password(password)
        self.click_login()
