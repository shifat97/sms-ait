import random

from faker import Faker

from api.teachers_api import get_teacher_filter

faker = Faker()


class TestEmailFilter:

    # Testing status code
    def test_email_filter_status_code(self, base_url, auth_header, created_teacher):
        email = created_teacher["email"]

        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="email",
                                      filter_value=email)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Testing search filter with email
    def test_get_teachers_email_filter(self, base_url, auth_header, created_teacher):
        email = created_teacher["email"]

        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="email",
                                      filter_value=email)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        teachers = response.json()
        # Validate teachers length - Must be 1
        assert len(teachers) == 1, f"Multiple response found: {teachers}"
        # Validate search email with response email
        assert teachers[0]["email"] == email, "Search email does not match"

    # Negative test

    # Search teacher with invalid email
    def test_get_teachers_email_filter_invalid_email(self, base_url, auth_header):
        email = faker.email()
        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="email",
                                      filter_value=email)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        # Validate response type
        assert isinstance(response.json(), list)
        # Validate response is empty
        assert len(response.json()) == 0, f"Found data with invalid email: {response.json()}"


class TestDepartmentFilter:
    valid_department_list = ["CSE", "BBA", "MBA", "LAW", "PHARMACY", "ENGLISH"]
    random_valid_department = random.choice(valid_department_list)

    invalid_department_list = ["SWE", "EEE", "ME"]
    random_invalid_department = random.choice(invalid_department_list)

    # Testing status code
    def test_department_filter_status_code(self, base_url, auth_header):
        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="department",
                                      filter_value=self.random_valid_department)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

    # Testing filter with valid department name
    def test_department_filter(self, base_url, auth_header):
        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="department",
                                      filter_value=TestDepartmentFilter.random_valid_department)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        data = response.json()

        # Validate data type
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        # Validate if all results equals to search string
        for d in data:
            # Validate data type
            assert isinstance(d, dict), f"Expected dict, got {type(d)}"

            # Validate name exists
            assert "name" in d, f"Missing field: name"
            # Validate name type
            assert isinstance(d["name"], str), f"Type mismatch: expected str, got {type(d['name'])}"
            # Validate email exists
            assert "email" in d, f"Missing field: email"
            # Validate email type
            assert isinstance(d["email"], str), f"Type mismatch: expected str, got {type(d['email'])}"
            # Validate teacherId exists
            assert "teacherId" in d, f"Missing field: teacherId"
            # Validate teacherId type
            assert isinstance(d["teacherId"], int), f"Type mismatch: expected int, got {type(d['teacherId'])}"

            # Validate department exists
            assert "department" in d, f"Missing field: department"
            # Validate department type
            assert isinstance(d["department"], str), f"Type mismatch: expected str, got {type(d['department'])}"
            # Validate department with search string
            assert d["department"].lower() == self.random_valid_department.lower(), \
                f"Value mismatch: expected {self.random_valid_department}, got {d['department']}"

    # Testing filter with invalid department name
    def test_department_with_invalid_department(self, base_url, auth_header):
        response = get_teacher_filter(base_url=base_url, auth_header=auth_header, filter_type="department",
                                      filter_value=TestDepartmentFilter.random_invalid_department)

        # Validate status code
        assert response.status_code == 404, f"Expected 404, Got {response.status_code}"

        data = response.json()

        # Validate type
        assert isinstance(data, dict), f"Expected list, got {type(data)}"
        # Validate message exits or not
        assert "message" in data or "error" in data, f"Missing field: message"
        # Validate message is null
        assert data["message"] or data["error"], "Message field should not be empty"
        # Validate message
        assert "invalid" in data["message"].lower() or "invalid" in data["error"].lower(), \
            f"Incorrect message: {data['message']}"


class TestFilterAuthorization:
    # Testing get teachers without authorization header
    def test_get_teacher_email_filter_without_authorization(self, base_url, auth_header, created_teacher):
        email = created_teacher["email"]

        response = get_teacher_filter(base_url=base_url, auth_header={}, filter_type="email", filter_value=email)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert response.json()["message"] == "Missing or invalid Authorization header", "Message is incorrect"

    # Testing get teachers filter with invalid token
    def test_get_teacher_with_invalid_token(self, base_url, auth_header, auth_header_with_invalid_token,
                                            created_teacher):
        email = created_teacher["email"]

        response = get_teacher_filter(base_url=base_url, auth_header=auth_header_with_invalid_token,
                                      filter_type="email", filter_value=email)

        # Validate status code
        assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
        # Validate message
        assert "Invalid" in response.json().get("message", "")
