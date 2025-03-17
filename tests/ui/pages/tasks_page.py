from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class TasksPage(BasePage):
    FLASH_MESSAGE_SUCCESS = (By.CSS_SELECTOR, '[data-testid="flash-message-success"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="nav-logout"]')

    def get_flash_success_message(self):
        return self.find_element(self.FLASH_MESSAGE_SUCCESS).text

    def click_logout_button(self):
        self.click_element(self.LOGOUT_BUTTON)

    def get_logout_button_text(self):
        return self.find_element(self.LOGOUT_BUTTON).text
