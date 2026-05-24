import random

from faker import Faker

faker = Faker()


def generate_random_department():
    list = ['CSE', 'BBA', 'MBA', 'LAW', 'PHARMACY', 'ENGLISH']
    department = random.choice(list)

    return department.upper()


def generate_random_designation():
    list = ['Assistant Professor', 'Associate Professor', 'Professor', 'Lecturer', 'Senior Lecturer']
    designation = random.choice(list)

    return designation.upper()


def generate_random_payload():
    """Data for add/teacher creation"""
    input_dict = {
        "name": f'Test {faker.first_name()}',
        "email": faker.email(),
        "department": generate_random_department(),
        "registrationId": faker.random_number() * 10000 + faker.random_number(),
        "age": random.randint(18, 100)
    }

    return input_dict
