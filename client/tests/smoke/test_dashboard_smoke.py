import pytest

from pages.dashboard_page import DashboardPage
from utils.random_payload_generator import generate_random_payload


class TestDashboard:
    @pytest.mark.smoke
    def test_add_student_with_valid_data(self, driver, auth_session):
        """Smoke: Can we add a student?"""
        page = DashboardPage(driver)

        page.click_add_button()

        # GET the random payload
        payload = generate_random_payload()

        """Add the student via form"""
        page.add_student_modal(
            name=payload['name'],
            email=payload['email'],
            registration_id=payload['registrationId'],
            age=payload['age']
        )

        assert page.is_visible(page.STUDENT_CREATION_SUCCESS), 'Student creation message not showing'
        assert 'created' in page.get_text(page.STUDENT_CREATION_SUCCESS).lower(), 'Message is invalid'

