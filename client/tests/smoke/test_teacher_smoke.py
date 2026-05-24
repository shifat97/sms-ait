import pytest

from pages.teachers_page import TeacherPage
from utils.random_payload_generator import generate_random_payload, generate_random_designation


class TestTeacher:
    @pytest.mark.smoke
    def test_add_teacher_with_valid_data(self, driver, auth_session):
        """Smoke: Can we add a teacher?"""
        page = TeacherPage(driver)

        page.click_add_button()

        # GET the random payload
        payload = generate_random_payload()
        designation = generate_random_designation()

        """Add the teacher via form"""
        page.add_teacher_modal(
            name=payload['name'],
            email=payload['email'],
            teacher_id=payload['registrationId'],
            designation=designation
        )

        assert page.is_visible(page.TEACHER_CREATION_SUCCESS), 'Teacher creation message not showing'
        assert 'created' in page.get_text(page.TEACHER_CREATION_SUCCESS).lower(), 'Message is invalid'

