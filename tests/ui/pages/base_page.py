import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)  # Ждем, пока элемент станет кликабельным
        )
        element.click()

    def enter_text(self, locator, text, timeout=10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

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

    def attach_screenshot(self, locator, name="screenshot"):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
