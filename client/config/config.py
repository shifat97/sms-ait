import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv('BASE_URL', 'https://example.com')
    TIMEOUT = int(os.getenv('TIMEOUT', 10))
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    # Test credentials (use .env for secrets)
    VALID_USERNAME = os.getenv('VALID_USERNAME', 'user@example.com')
    VALID_PASSWORD = os.getenv('VALID_PASSWORD', 'Secret123!')
