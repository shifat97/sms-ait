import requests

from utils.logger import logger_config

# POST
# Function for login
def login(base_url, payload):
    response = requests.post(f"{base_url}/login", json=payload)
    logger_config(response)
    return response
