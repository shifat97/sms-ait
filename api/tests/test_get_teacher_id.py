from faker import Faker

from api.teachers_api import get_teacher_id

faker = Faker()


class TestGetTeacherId:
    # Testing status code
    def test_get_teacher_id_status_code(self, base_url, auth_header, created_teacher):
        teacher_id = created_teacher["teacherId"]

        response = get_teacher_id(base_url=base_url, auth_header=auth_header, teacher_id=teacher_id)
        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Testing get teacher endpoint with id
    def test_get_teacher_id(self, base_url, auth_header, created_teacher, test_payload_structure):
        teacher_id = created_teacher["teacherId"]

        response = get_teacher_id(base_url=base_url, auth_header=auth_header, teacher_id=teacher_id)
        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        data = response.json()

        # Validate data type
        assert isinstance(data, dict), f"Expected dict, Got {type(data)}"
        # Validate _id
        assert data["teacherId"] == teacher_id, f"Expected {teacher_id}, Got {data['id']}"
        # Validate payload
        for key, value in created_teacher.items():
            # Validate if created key exits in the response
            assert key in data, f"Expected {key}, Got {data[key]}"
            # Validate create data and response data are same
            assert data[key] == value, f"Expected {value}, Got {data[key]}"
            # Validate if created fields are not empty
            assert data[key] is not None, f"Got null value for {key}"


class TestGetTeacherIdNegative:
    random_id = faker.random_number(digits=6)

    def test_get_teacher_with_invalid_id(self, base_url, auth_header):
        response = get_teacher_id(base_url=base_url, auth_header=auth_header, teacher_id=self.random_id)

        # Validate status code
        assert response.status_code == 404, f"Expected 404, Got {response.status_code}"
        # Validate type
        assert type(response.json()) == dict, f"Expected dict, Got {type(response.json())}"
        # Validate message
        assert response.json().get("error", "") == "Teacher not found", "Message is incorrect"

    def test_get_teacher_with_invalid_id_format(self, base_url, auth_header, created_teacher):
        teacher_id = created_teacher["_id"]
        response = get_teacher_id(base_url=base_url, auth_header=auth_header, teacher_id=teacher_id)

        # Validate status code
        assert response.status_code == 500, f"Expected 500, Got {response.status_code}"
        # Validate type
        assert type(response.json()) == dict, f"Expected dict, Got {type(response.json())}"
        # Validate error in response
        assert "error" in response.json(), "An error message must be present in the response body"


class TestGetTeacherAuthorization:
    # Testing get teachers without authorization header
    def test_get_teacher_without_authorization(self, base_url, created_teacher):
        teacher_id = created_teacher["teacherId"]
        response = get_teacher_id(base_url=base_url, auth_header={}, teacher_id=teacher_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()[
                   "message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing get teachers filter with invalid token
    def test_get_teacher_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token,
                                            created_teacher):
        teacher_id = created_teacher["teacherId"]
        response = get_teacher_id(base_url=base_url, auth_header=auth_header_with_invalid_token, teacher_id=teacher_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
