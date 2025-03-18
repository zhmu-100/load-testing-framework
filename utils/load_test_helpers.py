import random
from locust import HttpUser, task, between

def generate_user_data():
    return {
        "email": f"user{random.randint(1, 100000)}@test.com",
        "password": "test123"
    }

def make_request(client, endpoint, payload=None):
    with client.post(endpoint, json=payload, catch_response=True) as response:
        if response.status_code != 200:
            response.failure("Request failed")