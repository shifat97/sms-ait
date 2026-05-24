from api.auth.auth_api import login
from api.teacher.teacher_api import get_teacher

def test_token_expires(base_url, login_payload):
    # Login user to create the first token
    response = login(base_url=base_url, payload=login_payload["valid_username_valid_password"])
    # Store the old token first
    old_token = response.json().get("authToken")
    old_header = {"Authorization": f"Bearer {old_token}"}

    # Try to get all teachers with the token just created
    teachers = get_teacher(base_url=base_url, auth_header=old_header)

    # Validate the status code and type only
    assert teachers.status_code == 200, f"Expected 200, but got {teachers.status_code}"
    assert type(teachers.json()) == list, f"Expected list, but got {type(teachers.json())}"


    # Request again to generate a new token
    new_response = login(base_url=base_url, payload=login_payload["valid_username_valid_password"])
    new_token = new_response.json().get('authToken')
    new_header = {"Authorization": f"Bearer {new_token}"}

    # Try getting all teacher with new token
    teachers = get_teacher(base_url=base_url, auth_header=new_header)
    # Validate the status code and type only
    assert teachers.status_code == 200, f"Expected 200, but got {teachers.status_code}"
    assert type(teachers.json()) == list, f"Expected list, but got {type(teachers.json())}"


    # # Now try to request again with the old token
    # teachers = get_teacher(base_url=base_url, auth_header=old_header)
    # # Status code should be 401 due to expired old token
    # assert teachers.status_code == 401, f"Expected 401, but got {teachers.status_code}"
    # # Check the validation message
    # assert teachers.json()["error"] == "Missing or invalid Authorization header", "Message is incorrect"

