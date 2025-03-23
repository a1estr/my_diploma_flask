from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class ViewTaskPage(BasePage):
    TASK_TITLE = (By.CSS_SELECTOR, '[data-testid="task-title"]')
    TASK_DESCRIPTION = (By.CSS_SELECTOR, '[data-testid="task-description"]')
    TASK_STATUS = (By.CSS_SELECTOR, '[data-testid="task-status"]')
    TOGGLE_STATUS_BUTTON = (
        By.CSS_SELECTOR, '[data-testid="toggle-status-button"]'
    )
    BACK_BUTTON = (By.CSS_SELECTOR, '[data-testid="back-button"]')
    DELETE_BUTTON = (By.CSS_SELECTOR, '[data-testid="delete-button"]')
    DELETE_CONFIRM_BUTTON = (
        By.CSS_SELECTOR, '[data-testid="delete-confirm-button"]'
    )

    def get_title(self):
        return self.find_element(self.TASK_TITLE).text

    def get_description(self):
        return self.find_element(self.TASK_DESCRIPTION).text

    def get_task_status(self):
        return self.find_element(self.TASK_STATUS).text

    def toggle_status(self):
        self.click_element(self.TOGGLE_STATUS_BUTTON)

    def return_to_tasks_list(self):
        self.click_element(self.BACK_BUTTON)

    def click_delete_button(self):
        self.click_element(self.DELETE_BUTTON)

    def click_delete_confirm_button(self):
        self.click_element(self.DELETE_CONFIRM_BUTTON)
