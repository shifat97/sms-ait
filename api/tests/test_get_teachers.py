from api.teachers_api import get_teacher


class TestGetTeachers:
    # Testing endpoint to get all teachers
    def test_get_teachers_status_code(self, base_url, auth_header, teacher_payload):
        response = get_teacher(base_url=base_url, auth_header=auth_header)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Validate payload structure
    def test_get_teachers_payload_structure(self, base_url, auth_header, test_payload_structure):
        response = get_teacher(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        teachers = response.json()

        for teacher in teachers:
            for key, expected_type in test_payload_structure.items():
                key_type = type(teacher.get(key))

                # Validate if key in missing or not in the response
                assert key in teacher, f"{key} is missing on teacher: {teacher}"
                # Validate key type
                assert key_type == expected_type, f"Expected {expected_type}, Got {key_type}"
                # Validate if any value is null or not
                assert teacher[key] is not None, f"{teacher['_id']} on {key} has null value: {teacher[key]}"

    # Validate if duplicate id exists or not
    def test_get_teachers_duplicate_id(self, base_url, auth_header):
        response = get_teacher(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        teachers = response.json()

        ids = [teacher["teacherId"] for teacher in teachers]
        assert len(ids) == len(set(ids)), "Duplicate id exists in the list"

    # Validate if created teacher is in the list or not
    def test_get_teacher_after_creation(self, base_url, auth_header, created_teacher):
        response = get_teacher(base_url=base_url, auth_header=auth_header)

        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        teachers = response.json()

        ids = [teacher["teacherId"] for teacher in teachers]
        teacher_id = created_teacher["teacherId"]
        assert teacher_id in ids, f"{teacher_id} is not in the list after creation"


class TestGetTeacherAuthorization:
    # Testing get teachers without authorization header
    def test_get_teacher_without_authorization(self, base_url):
        response = get_teacher(base_url=base_url, auth_header={})

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()["message"] == "Missing or invalid Authorization header", "Message is incorrect"


    # Testing get teachers filter with invalid token
    def test_get_teacher_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token):
        response = get_teacher(base_url=base_url, auth_header=auth_header_with_invalid_token)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
