import os
import random

import pytest
import requests
from dotenv import load_dotenv
from faker import Faker

from api.teachers_api import create_teacher, delete_teacher_id

load_dotenv()
faker = Faker()


@pytest.fixture(scope="session")
def base_url():
    return f"{os.getenv('BASE_URL')}:{os.getenv('PORT')}"


@pytest.fixture(scope="session")
def login_payload():
    return {
        "valid_username_valid_password": {
            "username": os.getenv("ADMIN_USERNAME"),
            "password": os.getenv("ADMIN_PASSWORD")
        },
        "invalid_username_invalid_password": {
            "username": "admin123",
            "password": "ppppassword123"
        },
        "valid_username_invalid_password": {
            "username": "admin",
            "password": "passwordddd123"
        },
        "invalid_username_valid_password": {
            "username": "admin123",
            "password": "password123"
        }
    }


@pytest.fixture(scope="session")
def auth_header(base_url, login_payload):
    response = requests.post(f"{base_url}/login", json=login_payload["valid_username_valid_password"])
    auth_token = response.json().get('authToken')
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers


@pytest.fixture(scope="session")
def auth_header_with_invalid_token():
    return {
        "Authorization": f"Bearer {os.getenv('TEST_INVALID_TOKEN')}"
    }


@pytest.fixture
def teacher_payload():
    valid_department_list = ["CSE", "BBA", "MBA", "LAW", "PHARMACY", "ENGLISH"]
    random_department = random.choice(valid_department_list)
    designation_list = ["Assistant Professor", "Lecturer", "Senior Lecturer", "Associate Professor", "Professor"]
    random_designation = random.choice(designation_list)

    return {
        "valid_payload": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.first_name()+faker.email(),
            "department": random_department,
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
        "payload_without_name": {
            "email": faker.first_name()+faker.email(),
            "department": random_department,
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
        "payload_without_email": {
            "name": faker.first_name() + " " + faker.last_name(),
            "department": random_department,
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
        "payload_without_department": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.first_name()+faker.email(),
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
        "payload_without_teacher_id": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.first_name()+faker.email(),
            "department": random_department,
            "designation": random_designation
        },
        "payload_without_designation": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.first_name()+faker.email(),
            "department": random_department,
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4)
        },
        "payload_with_invalid_department": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": faker.first_name()+faker.email(),
            "department": "SWE",
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
        "payload_with_invalid_email": {
            "name": faker.first_name() + " " + faker.last_name(),
            "email": "johndoe#google.com",
            "department": "SWE",
            "teacherId": faker.unique.random_number(digits=6)+faker.unique.random_number(digits=4),
            "designation": random_designation
        },
    }


@pytest.fixture
def test_payload_structure():
    structure = {
        "_id": str,
        "name": str,
        "email": str,
        "department": str,
        "teacherId": int,
        "designation": str
    }

    return structure


@pytest.fixture
def created_teacher(base_url, auth_header, teacher_payload):
    response = create_teacher(
        base_url=base_url,
        auth_header=auth_header,
        payload=teacher_payload["valid_payload"]
    )

    yield response.json()

    delete_teacher_id(base_url, auth_header, response.json().get("teacherId"))
