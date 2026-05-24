import requests

from utils.logger import logger_config

# POST
# Function for post student endpoint
def create_student(base_url, auth_header, payload):
    response = requests.post(f"{base_url}/api/student", json=payload, headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for get student endpoint
def get_student(base_url, auth_header):
    response = requests.get(f"{base_url}/api/student", headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for student filter endpoint
def get_student_filter(base_url, auth_header, filter_type, filter_value):
    response = requests.get(f"{base_url}/api/student?{filter_type}={filter_value}", headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for get student by registrationId
def get_student_id(base_url, auth_header, registration_id):
    response = requests.get(f"{base_url}/api/student/{registration_id}", headers=auth_header)
    logger_config(response)
    return response


# PUT
# Function for update student by registrationId
def put_student_id(base_url, auth_header, payload, registration_id):
    response = requests.put(f"{base_url}/api/student/{registration_id}", json=payload, headers=auth_header)
    logger_config(response)
    return response


# DELETE
# Function for delete student by registrationId
def delete_student_id(base_url, auth_header, registration_id):
    response = requests.delete(f"{base_url}/api/student/{registration_id}", headers=auth_header)
    logger_config(response)
    return response
