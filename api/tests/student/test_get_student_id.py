from faker import Faker

from api.student.student_api import get_student_id

faker = Faker()


class TestGetStudentId:
    # Testing status code
    def test_get_student_id_status_code(self, base_url, auth_header, created_student):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url=base_url, auth_header=auth_header, registration_id=registration_id)
        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Testing get student endpoint with id
    def test_get_student_id(self, base_url, auth_header, created_student, test_student_payload_structure):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url=base_url, auth_header=auth_header, registration_id=registration_id)
        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        data = response.json()

        # Validate data type
        assert isinstance(data, dict), f"Expected dict, Got {type(data)}"
        # Validate registrationId
        assert data["registrationId"] == registration_id, f"Expected {registration_id}, Got {data['registrationId']}"
        # Validate payload
        for key, value in created_student.items():
            # Validate if created key exits in the response
            assert key in data, f"Expected {key}, Got {data[key]}"
            # Validate create data and response data are same
            assert data[key] == value, f"Expected {value}, Got {data[key]}"
            # Validate if created fields are not empty
            assert data[key] is not None, f"Got null value for {key}"


class TestGetStudentIdNegative:
    random_id = faker.random_number(digits=6)

    def test_get_student_with_invalid_id(self, base_url, auth_header):
        response = get_student_id(base_url=base_url, auth_header=auth_header, registration_id=self.random_id)

        # Validate status code
        assert response.status_code == 404, f"Expected 404, Got {response.status_code}"
        # Validate type
        assert type(response.json()) == dict, f"Expected dict, Got {type(response.json())}"
        # Validate message
        assert response.json().get("error", "") == "Student not found", "Message is incorrect"

    def test_get_student_with_invalid_id_format(self, base_url, auth_header, created_student):
        student_id = created_student["_id"]
        response = get_student_id(base_url=base_url, auth_header=auth_header, registration_id=student_id)

        # Validate status code
        assert response.status_code == 500, f"Expected 500, Got {response.status_code}"
        # Validate type
        assert type(response.json()) == dict, f"Expected dict, Got {type(response.json())}"
        # Validate error in response
        assert "error" in response.json(), "An error message must be present in the response body"


class TestGetStudentAuthorization:
    # Testing get students without authorization header
    def test_get_student_without_authorization(self, base_url, created_student):
        registration_id = created_student["registrationId"]
        response = get_student_id(base_url=base_url, auth_header={}, registration_id=registration_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()[
                   "message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing get students with invalid token
    def test_get_student_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token,
                                            created_student):
        registration_id = created_student["registrationId"]
        response = get_student_id(base_url=base_url, auth_header=auth_header_with_invalid_token,
                                  registration_id=registration_id)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
