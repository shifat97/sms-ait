import requests
from api.auth.auth_api import login


# Positive tests

# Test login with valid credentials
def test_login_with_valid_credentials(base_url, login_payload):
    response = login(base_url=base_url, payload=login_payload["valid_username_valid_password"])

    data = response.json()
    # Validate the status code
    assert response.status_code == 200, f"Expected 200, Got {response.status_code}"
    # Validate if token is exits in the response
    assert "authToken" in data, "Token is missing in the response"
    # Validate if token is empty or not
    assert data["authToken"], "Token is empty"


# Negative tests

# Test login with invalid username and password
def test_login_with_invalid_credentials(base_url, login_payload):
    response = login(base_url=base_url, payload=login_payload["valid_username_invalid_password"])

    data = response.json()
    # Validate status code
    assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
    # Validate message exits or not
    assert "message" in data, "Message is missing in the response"
    # Validate message is not empty
    assert data["message"], "Message is empty"
    # Validate message
    assert data["message"] == "Invalid credentials", f"Expected {'Invalid credentials'}, Got {data['message']}"


# Test login with valid username and invalid password
def test_login_with_valid_username_invalid_password(base_url, login_payload):
    response = login(base_url=base_url, payload=login_payload["invalid_username_valid_password"])

    data = response.json()
    # Validate status code
    assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
    # Validate message exits or not
    assert "message" in data, "Message is missing in the response"
    # Validate message is not empty
    assert data["message"], "Message is empty"
    # Validate message
    assert data["message"] == "Invalid credentials", f"Expected {'Invalid credentials'}, Got {data['message']}"


# Test login with invalid username and valid password
def test_login_with_invalid_username_valid_password(base_url, login_payload):
    response = login(base_url=base_url, payload=login_payload["invalid_username_invalid_password"])

    data = response.json()
    # Validate status code
    assert response.status_code == 401, f"Expected 401, Got {response.status_code}"
    # Validate message exits or not
    assert "message" in data, "Message is missing in the response"
    # Validate message is not empty
    assert data["message"], "Message is empty"
    # Validate message
    assert data["message"] == "Invalid credentials", f"Expected {'Invalid credentials'}, Got {data['message']}"
