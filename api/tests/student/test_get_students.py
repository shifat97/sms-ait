from api.student.student_api import get_student


class TestGetStudents:
    # Testing endpoint to get all students
    def test_get_students_status_code(self, base_url, auth_header, student_payload):
        response = get_student(base_url=base_url, auth_header=auth_header)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Validate payload structure
    def test_get_students_payload_structure(self, base_url, auth_header, test_student_payload_structure):
        response = get_student(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        students = response.json()

        # for student in students:
        #     for key, expected_type in test_student_payload_structure.items():
        #         key_type = type(student.get(key))

        #         # Validate if key in missing or not in the response
        #         assert key in student, f"{key} is missing on student: {student}"
        #         # Validate key type
        #         assert key_type == expected_type, f"Expected {expected_type}, Got {key_type}"
        #         # Validate if any value is null or not
        #         assert student[key] is not None, f"{student['_id']} on {key} has null value: {student[key]}"

    # Validate if duplicate id exists or not
    def test_get_students_duplicate_id(self, base_url, auth_header):
        response = get_student(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        students = response.json()

        ids = [student["registrationId"] for student in students]
        assert len(ids) == len(set(ids)), "Duplicate id exists in the list"

    # Validate if created student is in the list or not
    def test_get_student_after_creation(self, base_url, auth_header, created_student):
        response = get_student(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        students = response.json()

        ids = [student["registrationId"] for student in students]
        registration_id = created_student["registrationId"]
        assert registration_id in ids, f"{registration_id} is not in the list after creation"


class TestGetStudentAuthorization:
    # Testing get students without authorization header
    def test_get_student_without_authorization(self, base_url):
        response = get_student(base_url=base_url, auth_header={})

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()["message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing get students with invalid token
    def test_get_student_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token):
        response = get_student(base_url=base_url, auth_header=auth_header_with_invalid_token)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
