from selenium.webdriver.common.by import By
from tests.ui.pages.base_page import BasePage


class TasksPage(BasePage):
    FLASH_MESSAGE_SUCCESS = (By.CSS_SELECTOR, '[data-testid="flash-message-success"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="nav-logout"]')
    CREATE_TASK_BUTTON = (By.CSS_SELECTOR, '[data-testid="create-task-button"]')
    CREATE_FIRST_TASK_BUTTON = (By.CSS_SELECTOR, '[data-testid="create-first-task-link"]')
    CREATE_TASK_NAV_BUTTON = (By.CSS_SELECTOR, '[data-testid="nav-create-task"]')
    NO_TASKS_MESSAGE = (By.CSS_SELECTOR, '[data-testid="no-tasks-message"]')
    TASK_TITLE = (By.CSS_SELECTOR, "h5.card-title.mb-0")
    EDIT_TASK_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-sm.btn-warning")
    VIEW_TASK_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-sm.btn-info")
    TASK_CARD = (By.CSS_SELECTOR, ".card.h-100")

    def get_flash_success_message(self):
        return self.find_element(self.FLASH_MESSAGE_SUCCESS).text

    def click_create_task_button(self):
        self.click_element(self.CREATE_TASK_BUTTON)

    def get_task_titles_list(self):
        tasks = self.get_elements(self.TASK_TITLE)
        task_titles_list = []
        for task in tasks:
            task_titles_list.append(task.text)
        return task_titles_list

    def get_task_cards(self):
        return self.get_elements(self.TASK_CARD)

    def click_edit_button(self, task_title):
        tasks = self.get_task_cards()
        for task in tasks:
            actual_title = self.find_element(self.TASK_TITLE).text
            if actual_title == task_title:
                self.click_element(self.EDIT_TASK_BUTTON)
                return

    def click_view_button(self, task_title):
        tasks = self.get_task_cards()
        for task in tasks:
            actual_title = self.find_element(self.TASK_TITLE).text
            if actual_title == task_title:
                self.click_element(self.VIEW_TASK_BUTTON)
                return

    def click_logout_button(self):
        self.click_element(self.LOGOUT_BUTTON)

    def get_logout_button_text(self):
        return self.find_element(self.LOGOUT_BUTTON).text
