import time

import pytest

from pages.dashboard_page import DashboardPage
from utils.random_payload_generator import generate_random_payload
from utils.table_filter_handler import table_filter
from utils.table_reload_handler import wait_for_table_to_contain_rows


class TestDashboard:
    @pytest.mark.regression
    def test_eye_button_to_toggle_visibility(self, driver, auth_session):
        """Regression: Can we toggle the visibility of the table?"""
        page = DashboardPage(driver)

        page.click_add_button()
        payload = generate_random_payload()

        """Add the student via form"""
        created_payload = page.add_student_modal(
            name=payload['name'],
            email=payload['email'],
            registration_id=payload['registrationId'],
            age=payload['age']
        )

        assert page.is_visible(page.STUDENT_CREATION_SUCCESS), f'Student creation message not showing'
        # page.wait_until_invisible(DashboardPage.MODAL)
        # page.wait_until_invisible(page.STUDENT_CREATION_SUCCESS)
        time.sleep(1)

        page.search_student_with_email(payload['email'])

        rows = page.find_all(page.TABLE_ROW)
        assert len(rows) == 1, f'Expected 1 row, Got {rows}'

        # Click on the eye button
        page.click_view_button()

        list_of_text = [element.text for element in page.find_all(page.VIEW_CONTAINER_TEXTS)]

        view_payload = {
            "name": list_of_text[0],
            "email": list_of_text[1],
            "department": list_of_text[2],
            "registrationId": int(list_of_text[3]),
            "age": int(list_of_text[4])
        }

        assert created_payload == view_payload, f"Expected {created_payload}, Got {view_payload}"


    @pytest.mark.regression
    def test_search_with_name_student_after_creation(self, driver, auth_session):
        """Regression: Can we search with a name?"""
        page = DashboardPage(driver)

        page.click_add_button()
        payload = generate_random_payload()

        """Add the student via form"""
        created_payload = page.add_student_modal(
            name=payload['name'],
            email=payload['email'],
            registration_id=payload['registrationId'],
            age=payload['age']
        )

        assert page.is_visible(page.STUDENT_CREATION_SUCCESS), 'Student creation message not showing'
        time.sleep(1)

        page.search_student_with_name(payload['name'])
        wait_for_table_to_contain_rows(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)

        results = table_filter(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)
        for data in results:
            assert created_payload['name'] in data['name'], \
                f"Expected {created_payload['name']}, Got {data['name']}"

    @pytest.mark.regression
    def test_search_with_email_student_after_creation(self, driver, auth_session):
        """Regression: Can we search with email?"""
        page = DashboardPage(driver)

        page.click_add_button()
        payload = generate_random_payload()

        # Add the student via form
        created_payload = page.add_student_modal(
            name=payload['name'],
            email=payload['email'],
            registration_id=payload['registrationId'],
            age=payload['age']
        )

        assert page.is_visible(page.STUDENT_CREATION_SUCCESS), 'Student creation message not showing'
        time.sleep(1)

        page.search_student_with_email(payload['email'])
        wait_for_table_to_contain_rows(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)

        result = table_filter(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)
        assert len(result) == 1, f"Expected 1 result, Got {len(result)}"
        assert created_payload['email'] in result[0]['email'], f"Expected {created_payload['email']}, Got {result[0]['email']}"
        assert created_payload['email'] == result[0]['email'], f"Expected {created_payload['email']}, Got {result[0]['email']}"

    @pytest.mark.regression
    def test_filter_with_department(self, driver, auth_session):
        """Regression: Can we filter with department?"""
        page = DashboardPage(driver)
        page.click(DashboardPage.STUDENTS_NAV_MENU)

        assert page.is_loaded()
        assert '/dashboard' in page.current_url

        page.page_size_dropdown("100")

        department = page.department_dropdown(page.DEPARTMENT_FILTER_BUTTON)
        page.click_filter()

        wait_for_table_to_contain_rows(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)

        table_data = []

        while True:
            rows = table_filter(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)
            table_data.extend(rows)

            next_btn = page.find(DashboardPage.NEXT_BUTTON)
            if next_btn.get_attribute('disabled'):
                break

            next_btn.click()

        for d in table_data:
            assert d["department"] == department, \
                f'Expected {department}, Got {d["department"]} for id {d["registration_id"]}'

    @pytest.mark.regression
    def test_search_with_registration_id_after_creation(self, driver, auth_session):
        """Regression: Can we search with registration id?"""
        page = DashboardPage(driver)

        page.click_add_button()
        payload = generate_random_payload()

        # Add the student via form
        created_payload = page.add_student_modal(
            name=payload['name'],
            email=payload['email'],
            registration_id=payload['registrationId'],
            age=payload['age']
        )

        assert page.is_visible(page.STUDENT_CREATION_SUCCESS), 'Student creation message not showing'
        time.sleep(1)

        page.search_student_with_registration_id(payload['registrationId'])

        wait_for_table_to_contain_rows(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)

        result = table_filter(driver, DashboardPage.TABLE_ROW, DashboardPage.TABLE_COLUMN)
        assert len(result) == 1, f"Expected 1 result, Got {len(result)}"
        assert int(created_payload['registrationId']) == int(result[0]['registrationId']), \
                f"Expected {int(created_payload['registrationId'])}, Got {int(result[0]['registrationId'])}"
