from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from config.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)

    def visit(self, path=''):
        self.driver.get(Config.BASE_URL + path)
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_until_visible(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_all_visible(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_until_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    # def click(self, locator):
    #     for _ in range(3):
    #         try:
    #             self.wait.until(EC.element_to_be_clickable(locator)).click()
    #             return self
    #         except StaleElementReferenceException:
    #             continue
    #     self.wait.until(EC.element_to_be_clickable(locator)).click()
    #     return self

    def type_text(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
        return self

    def get_text(self, locator):
        return self.find(locator).text

    def select_by_text(self, locator, text):
        dropdown = Select(self.find(locator))
        dropdown.select_by_visible_text(text)
        return self

    def select_by_value(self, locator, value):
        dropdown = Select(self.find(locator))
        dropdown.select_by_value(value)
        return self

    def is_visible(self, locator):
        try:
            return self.find(locator).is_displayed()
        except:
            return False

    def wait_for_url(self, fragment):
        self.wait.until(EC.url_contains(fragment))
        return self

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title
