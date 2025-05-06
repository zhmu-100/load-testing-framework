from locust import HttpUser, task, between
import json
import random
import datetime
import threading
import base64
import jwt
import os

# Конфигурация хоста и сервисов
GATEWAY_HOST = "http://188.225.77.13:8080"  # Только для auth
SERVICES = {
    "profile": "http://188.225.77.13:8083",
    "training": "http://188.225.77.13:8084",
    "diet": "http://188.225.77.13:8087",
    "feed": "http://188.225.77.13:8085",
    "notes": "http://188.225.77.13:8086",
    "statistics": "http://188.225.77.13:8088",
    "db": "http://188.225.77.13:8090",
}

created_users_lock = threading.Lock()
created_users = set()

JWT_SECRET = os.getenv("JWT_SECRET", "development_secret_key")
JWT_ALGORITHM = "HS256"
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "mad-mobile-app")

def generate_user_credentials():
    user_id = random.randint(1, 10_000)
    username = f"testuser_{user_id:05}"
    mail = f"testuser_{username}@mail.ru"
    return username, "password", mail


class MadUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        username, password, mail = generate_user_credentials()

        with created_users_lock:
            if username not in created_users:
                reg_resp = self.client.post(f"{GATEWAY_HOST}/api/auth/register", json={
                    "username": username,
                    "email": mail,
                    "password": password
                })
                print(f"Register response: {reg_resp.status_code} - {reg_resp.text}")
                created_users.add(username)

        response = self.client.post(f"{GATEWAY_HOST}/api/auth/login", json={
            "username": username,
            "password": password
        })
        print(f"Login response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            try:
                self.token = response.json().get("token")
                if not self.token:
                    raise ValueError("No token in login response")
                self.user_id = self.extract_user_id_from_jwt(self.token)
            except Exception as e:
                print(f"Failed to extract token: {e}")
                self.token = ""
                self.user_id = "test-user-id"
        else:
            self.token = ""
            self.user_id = "test-user-id"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def extract_user_id_from_jwt(self, token):
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE, options={"verify_aud": False})
            return decoded.get("sub") or decoded.get("userId") or decoded.get("id")
        except Exception as e:
            print(f"JWT decode failed: {e}")
            return "test-user-id"

    @task
    def get_profile(self):
        self.client.get(f"{SERVICES['profile']}/profiles", headers=self.headers)

    @task
    def create_note(self):
        self.client.post(f"{SERVICES['notes']}/notebook/notes", headers=self.headers, json={
            "userId": "user123",
            "title": "Test Note",
            "content": "Load test content",
        })

    @task
    def list_workouts(self):
        self.client.get(f"{SERVICES['training']}/training/workouts", headers=self.headers)

    @task
    def create_post(self):
        self.client.post(f"{SERVICES['feed']}/posts", headers=self.headers, json={
            "post": {
                "userId": "user123",
                "content": "user123 first post",
                "attachments": []
            }
        })

    @task
    def list_foods(self):
        self.client.get(f"{SERVICES['diet']}/diet/foods", headers=self.headers)

    @task
    def upload_calories(self):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.client.post(f"{SERVICES['statistics']}/statistics/calories", headers=self.headers, json={
            "meta": {
                "id": "cal-123",
                "userId": "user-001",
                "timestamp": now
            },
            "calories": random.uniform(100, 500)
        })

    @task
    def query_database(self):
        self.client.post(f"{SERVICES['db']}/read", headers=self.headers, json={
            "table": "meals",
            "columns": ["id"],
            "filters": {}
        })
