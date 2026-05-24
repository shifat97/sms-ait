from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = '/signin'
    TITLE = (By.XPATH, "//h3[text()='Sign In']")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "[type='submit']")
    ERROR_MSG = (By.XPATH, "//form//div[text()='Please enter both username and password']")
    INVALID_CREDENTIAL = (By.XPATH, "//form//div[text()='Invalid credentials']")

    def open(self):
        return self.visit(self.PATH)

    def login(self, email, password):
        self.type_text(self.USERNAME, email)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return self

    def get_error(self):
        return self.get_text(self.ERROR_MSG)

    def get_invalid_credentials(self):
        return self.get_text(self.INVALID_CREDENTIAL)
