import requests

from utils.logger import logger_config

# POST
# Function for post teacher endpoint
def create_teacher(base_url, auth_header, payload):
    response = requests.post(f"{base_url}/api/teacher", json=payload, headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for get teacher endpoint
def get_teacher(base_url, auth_header):
    response = requests.get(f"{base_url}/api/teacher", headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for email filter endpoint
def get_teacher_filter(base_url, auth_header, filter_type, filter_value):
    response = requests.get(f"{base_url}/api/teacher?{filter_type}={filter_value}", headers=auth_header)
    logger_config(response)
    return response


# GET
# Function for get teacher by id
def get_teacher_id(base_url, auth_header, teacher_id):
    response = requests.get(f"{base_url}/api/teacher/{teacher_id}", headers=auth_header)
    logger_config(response)
    return response


# PUT
# Function for update teacher by id
def put_teacher_id(base_url, auth_header, payload, teacher_id):
    response = requests.put(f"{base_url}/api/teacher/{teacher_id}", json=payload, headers=auth_header)
    logger_config(response)
    return response

# DELETE
# Function for delete teacher by id
def delete_teacher_id(base_url, auth_header, teacher_id):
    response = requests.delete(f"{base_url}/api/teacher/{teacher_id}", headers=auth_header)
    logger_config(response)
    return response
