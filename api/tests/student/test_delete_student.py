import random

from api.student.student_api import delete_student_id, get_student


class TestDeleteStudent:
    random_id = None

    def test_delete_student(self, base_url, auth_header):
        get_all_students_response = get_student(base_url, auth_header)
        # Validate status code
        assert get_all_students_response.status_code == 200, f"Expected 200, got {get_all_students_response.status_code}"

        get_all_students = get_all_students_response.json()
        # Validate response type
        assert type(get_all_students) == list, f"Expected list, got {type(get_all_students)}"

        # Get all id
        ids = [student["registrationId"] for student in get_all_students]
        # Select a random id
        TestDeleteStudent.random_id = random.choice(ids)

        # Call delete API
        after_delete = delete_student_id(base_url, auth_header, self.random_id)

        # Validate status code
        assert after_delete.status_code == 200, f"Expected 200, got {after_delete.status_code}"

        after_delete_json = after_delete.json()
        # Validate response type
        assert type(after_delete_json) == dict, f"Expected dict, got {type(after_delete_json)}"
        # Validate message
        assert after_delete_json["message"] == "Student deleted successfully", "Message is incorrect"

    def test_get_student_after_delete(self, base_url, auth_header):
        response = delete_student_id(base_url, auth_header, TestDeleteStudent.random_id)

        # Validate status code
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        response_json = response.json()
        # Validate error in response
        assert "error" in response_json, f"Error field should be available in response"
        # Validate message
        assert response_json["error"] == "Student not found", "Message is incorrect"


class TestDeleteStudentAuthorization:
    # Testing delete students without authorization header
    def test_delete_student_without_authorization(self, base_url):
        response = delete_student_id(base_url=base_url, auth_header={}, registration_id=TestDeleteStudent.random_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()[
                   "message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing delete students with invalid token
    def test_delete_student_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token):
        response = delete_student_id(base_url=base_url, auth_header=auth_header_with_invalid_token,
                                     registration_id=TestDeleteStudent.random_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
