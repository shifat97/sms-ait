import random

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    PATH = '/dashboard/students'
    DASHBOARD_TITLE = (By.XPATH, "//div//h1[text()='Students']")
    LOGOUT_BTN = (By.XPATH, "//div[@data-sidebar='footer']//button")
    STUDENTS_NAV_MENU = (By.XPATH, "//ul//li//a[.//span[text()='Students']]")
    SELECT_PAGE_SIZE = (By.XPATH, "//div//select")
    DEPARTMENT_FILTER_BUTTON = (By.XPATH, "//button[@role='combobox']")
    FILTER_OPTIONS = (By.XPATH, "//div[@role='option']")
    FILTER_BUTTON = (By.XPATH, "//button[text()='Filter']")
    TABLE = (By.XPATH, "//table")
    TABLE_BODY = (By.XPATH, "//table//tbody")
    TABLE_ROW = (By.XPATH, "//table//tbody//tr")
    TABLE_COLUMN = (By.XPATH, "./td")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    LOADING_SPINNER = (By.XPATH, "//table//tbody//tr//td//*[local-name()='svg']")
    ADD_STUDENT_BTN = (By.XPATH, "//div//button[normalize-space()='Add Student']")
    MODAL = (By.XPATH, "//div[@role='dialog']")
    MODAL_NAME = (By.ID, "name")
    MODAL_EMAIL = (By.ID, "email")
    MODAL_DEPARTMENT = (By.XPATH, "//div//select[preceding-sibling::button]")
    MODAL_REGISTRATION_ID = (By.ID, 'registrationId')
    MODAL_AGE = (By.ID, 'age')
    MODAL_CREATE_BTN = (By.XPATH, "//button[contains(text(), 'Create')]")
    MODAL_FILTER_BTN = (By.XPATH, "//div//button[following-sibling::select]")
    STUDENT_CREATION_SUCCESS = (By.XPATH, "//div//section//ol//li[normalize-space()='Student created']")
    FILTER_NAME_INPUT = (By.CSS_SELECTOR, "[placeholder='Filter by name...']")
    FILTER_EMAIL_INPUT = (By.CSS_SELECTOR, "[placeholder='Filter by email...']")
    FILTER_REGISTRATION_ID_INPUT = (By.CSS_SELECTOR, "[placeholder='Filter by registration id...']")
    ROW_VIEW_BTN = (By.XPATH, ".//button[.//*[contains(@class,'lucide-eye')]]")
    ROW_EDIT_BTN = (By.XPATH, ".//button[.//*[contains(@class,'lucide-pencil')]]")
    ROW_DELETE_BTN = (By.XPATH, ".//button[.//*[contains(@class,'lucide-trash2')]]")
    VIEW_CONTAINER_TEXTS = (By.XPATH, "//div//div//span[preceding-sibling::span]")

    def is_loaded(self):
        return self.is_visible(self.DASHBOARD_TITLE)

    def get_page_title(self):
        return self.get_text(self.DASHBOARD_TITLE)

    def click_filter(self):
        self.click(self.FILTER_BUTTON)
        return self

    def click_add_button(self):
        self.click(self.ADD_STUDENT_BTN)
        return self

    def click_view_button(self):
        self.click(self.ROW_VIEW_BTN)
        return self

    def click_edit_button(self):
        self.click(self.ROW_EDIT_BTN)
        return self

    def click_delete_button(self):
        self.click(self.ROW_DELETE_BTN)
        return self

    def add_student_modal(self, name, email, registration_id, age):
        self.type_text(self.MODAL_NAME, name)
        self.type_text(self.MODAL_EMAIL, email)
        dropdown_value = self.department_dropdown(self.MODAL_FILTER_BTN)
        self.type_text(self.MODAL_REGISTRATION_ID, registration_id)
        self.type_text(self.MODAL_AGE, age)
        self.click(self.MODAL_CREATE_BTN)
        return {
            "name": name,
            "email": email,
            "department": dropdown_value,
            "registrationId": registration_id,
            "age": age
        }

    def search_student_with_name(self, name):
        self.type_text(self.FILTER_NAME_INPUT, name)
        self.click(self.FILTER_BUTTON)
        return self

    def search_student_with_email(self, email):
        self.type_text(self.FILTER_EMAIL_INPUT, email)
        self.click(self.FILTER_BUTTON)
        return self

    def search_student_with_registration_id(self, id):
        self.type_text(self.FILTER_REGISTRATION_ID_INPUT, id)
        self.click(self.FILTER_BUTTON)
        return self

    def logout(self):
        self.click(self.LOGOUT_BTN)
        return self

    def page_size_dropdown(self, page_size):
        self.select_by_value(self.SELECT_PAGE_SIZE, page_size)
        return self

    def department_dropdown(self, locator):
        self.click(locator)
        departments = self.find_all(self.FILTER_OPTIONS)
        department = random.choice(departments)
        selected_value = department.text
        department.click()
        return selected_value
