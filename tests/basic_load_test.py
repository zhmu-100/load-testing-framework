from locust import HttpUser, task, between
from utils.load_test_helpers import generate_user_data, make_request

class LoadTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def register_user(self):
        data = generate_user_data()
        make_request(self.client, "/api/register", data)