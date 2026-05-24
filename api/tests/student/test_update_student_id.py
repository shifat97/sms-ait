from faker import Faker

from api.student.student_api import get_student_id, put_student_id

faker = Faker()


class TestPutStudentId:
    def test_put_student_with_valid_info(self, base_url, auth_header, created_student, test_student_payload_structure):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url, auth_header, registration_id)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        # Validate response type
        student_before_update = response.json()
        assert type(student_before_update) == dict, f"Expected dict, Got {type(student_before_update)}"

        new_payload = {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.email(),
            "department": created_student["department"],
            "age": created_student["age"],
        }

        student_after_update = put_student_id(base_url=base_url, auth_header=auth_header, payload=new_payload,
                                              registration_id=registration_id)

        # Validate status code after update
        assert student_after_update.status_code == 200, f"Expected 200, Got {student_after_update.status_code}"
        # Validate response type
        new_response = student_after_update.json()
        assert type(new_response) == dict, f"Expected dict, Got {type(new_response)}"

        # Validate id after update
        assert new_response["_id"] == student_before_update[
            "_id"], f"Expected {student_before_update['_id']}, Got {new_response['_id']}"

        # Validate old data is not matched with new data
        assert student_before_update["name"] != new_response["name"], "Name field matched after update"
        assert student_before_update["email"] != new_response["email"], "Email field matched after update"

        # Validate payload after update
        for key, value in new_payload.items():
            assert value == new_response[key], f"Expected {new_payload[key]}, Got {new_response[key]}"
            assert new_response[key] is not None, f"Expected {value}, Got {value}"

        # Validate data types
        for k1, v1 in new_response.items():
            actual_type = type(v1)
            for k2, v2 in test_student_payload_structure.items():
                expected_type = test_student_payload_structure[k1]
                assert actual_type == expected_type, f"Expected {expected_type}, Got {actual_type}"


class TestPutStudentNegative:
    def test_put_student_with_id(self, base_url, auth_header, created_student):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url, auth_header, registration_id)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        student_before_update = response.json()
        # Validate response type
        assert type(student_before_update) == dict, f"Expected dict, Got {type(student_before_update)}"

        new_payload = {
            "_id": faker.uuid4()
        }

        new_response = put_student_id(base_url, auth_header, new_payload, registration_id)

        # Validate status code
        assert new_response.status_code == 400, f"Expected 400, Got {new_response.status_code}"
        # Validate error in response
        assert "error" in new_response.json(), f"Error should available in the response"

    def test_put_student_with_registration_id(self, base_url, auth_header, created_student):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url, auth_header, registration_id)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"

        student_before_update = response.json()
        # Validate response type
        assert type(student_before_update) == dict, f"Expected dict, Got {type(student_before_update)}"

        new_payload = {
            "registrationId": faker.uuid4()
        }

        new_response = put_student_id(base_url, auth_header, new_payload, registration_id)

        # Validate status code
        assert new_response.status_code == 400, f"Expected 400, Got {new_response.status_code}"
        # Validate error in response
        assert "error" in new_response.json(), f"Error should available in the response"


class TestPutStudentIdAuthorization:
    def test_put_student_without_auth_header(self, base_url, auth_header, created_student):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url, auth_header, registration_id)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        # Validate response type
        student_before_update = response.json()
        assert type(student_before_update) == dict, f"Expected dict, Got {type(student_before_update)}"

        new_payload = {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.email(),
            "department": created_student["department"],
            "age": created_student["age"],
        }

        student_after_update = put_student_id(base_url=base_url, auth_header={}, payload=new_payload,
                                              registration_id=registration_id)

        # Validate status code
        assert student_after_update.status_code == 401, f"Expected 401, Got {student_after_update.status_code}"
        # Validate message
        assert student_after_update.json()[
                   "message"] == "Missing or invalid Authorization header", "Message is incorrect"

    def test_put_student_with_invalid_token(self, base_url, auth_header, created_student,
                                            auth_header_with_invalid_token):
        registration_id = created_student["registrationId"]

        response = get_student_id(base_url, auth_header, registration_id)

        # Validate status code
        assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
        # Validate response type
        student_before_update = response.json()
        assert type(student_before_update) == dict, f"Expected dict, Got {type(student_before_update)}"

        new_payload = {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.email(),
            "department": created_student["department"],
            "age": created_student["age"],
        }

        student_after_update = put_student_id(base_url=base_url, auth_header=auth_header_with_invalid_token,
                                              payload=new_payload,
                                              registration_id=registration_id)

        # Validate status code
        assert student_after_update.status_code == 401, f"Expected 401, Got {student_after_update.status_code}"
        # Validate message
        assert student_after_update.json()["message"] == "Invalid or expired token", "Message is incorrect"
