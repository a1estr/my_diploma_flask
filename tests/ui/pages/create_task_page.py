from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class CreateTaskPage(BasePage):
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="submit-button"]')
    TASK_TITLE = (By.CSS_SELECTOR, '[data-testid="title-input"]')
    TASK_DESCRIPTION = (By.CSS_SELECTOR, '[data-testid="description-input"]')
    TASK_HEADER = (By.CLASS_NAME, "card-header")

    def enter_title(self, title):
        self.enter_text(self.TASK_TITLE, title)

    def enter_description(self, description):
        self.enter_text(self.TASK_DESCRIPTION, description)

    def click_submit_button(self):
        self.click_element(self.SUBMIT_BUTTON)

    def get_task_header_text(self):
        return self.find_element(self.TASK_HEADER).text
