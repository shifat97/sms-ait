import random

from api.teachers_api import delete_teacher_id, get_teacher


class TestDeleteTeacher:
    random_id = None

    def test_delete_teacher(self, base_url, auth_header):
        get_all_teachers_response = get_teacher(base_url, auth_header)
        # Validate status code
        assert get_all_teachers_response.status_code == 200, f"Expected 200, got {get_all_teachers_response.status_code}"

        get_all_teachers = get_all_teachers_response.json()
        # Validate response type
        assert type(get_all_teachers) == list, f"Expected list, got {type(get_all_teachers)}"

        # Get all id
        ids = [teacher["teacherId"] for teacher in get_all_teachers]
        # Select a random id
        TestDeleteTeacher.random_id = random.choice(ids)

        # Call delete API
        after_delete = delete_teacher_id(base_url, auth_header, self.random_id)

        # Validate status code
        assert after_delete.status_code == 200, f"Expected 200, got {after_delete.status_code}"

        after_delete_json = after_delete.json()
        # Validate response type
        assert type(after_delete_json) == dict, f"Expected dict, got {type(after_delete_json)}"
        # Validate message
        assert after_delete_json["message"] == "Teacher deleted successfully", "Message is incorrect"

    def test_get_teacher_after_delete(self, base_url, auth_header):
        response = delete_teacher_id(base_url, auth_header, TestDeleteTeacher.random_id)

        # Validate status code
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        response_json = response.json()
        # Validate error in response
        assert "error" in response_json, f"Error field should be available in response"
        # Validate message
        assert response_json["error"] == "Teacher not found", "Message is incorrect"


class TestDeleteTeacherAuthorization:
    # Testing get teachers without authorization header
    def test_get_teacher_without_authorization(self, base_url):
        response = delete_teacher_id(base_url=base_url, auth_header={}, teacher_id=TestDeleteTeacher.random_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()[
                   "message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing get teachers filter with invalid token
    def test_get_teacher_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token):
        response = delete_teacher_id(base_url=base_url, auth_header=auth_header_with_invalid_token,
                                     teacher_id=TestDeleteTeacher.random_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
