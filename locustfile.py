from locust import HttpUser, task, between
import json
import random
import datetime
import threading
import base64
import jwt 
import os

created_users_lock = threading.Lock()
created_users = set()

JWT_SECRET = os.getenv("JWT_SECRET", "development_secret_key")
JWT_ALGORITHM = "HS256"
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "mad-mobile-app")

def generate_user_credentials():
    user_id = random.randint(1, 10_000)
    username = f"testuser_{user_id:05}"
    return username, "password"


class MadUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        username, password = generate_user_credentials()

        with created_users_lock:
            if username not in created_users:
                self.client.post("/api/auth/register", json={
                    "username": username,
                    "password": password
                })
                created_users.add(username)

        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": password
        })

        self.token = response.json().get("token") or "<HARDCODED_JWT_TOKEN>"
        self.user_id = self.extract_user_id_from_jwt(self.token)
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
        self.client.get("/api/profiles/me", headers=self.headers)

    @task
    def create_note(self):
        now = datetime.datetime.utcnow().isoformat()
        self.client.post("/api/notebook/notes", headers=self.headers, json={
            "title": "Test Note",
            "content": "Load test content",
            "date": now
        })

    @task
    def list_workouts(self):
        self.client.get("/api/training/workouts", headers=self.headers)

    @task
    def create_post(self):
        self.client.post("/api/feed/posts", headers=self.headers, json={
            "content": "Testing post from locust",
            "attachments": []
        })

    @task
    def list_foods(self):
        self.client.get("/api/diet/foods", headers=self.headers)

    @task
    def upload_calories(self):
        now = datetime.datetime.utcnow().isoformat()
        self.client.post("/api/statistics/calories", headers=self.headers, json={
            "meta": {
                "userId": self.user_id,
                "timestamp": now
            },
            "calories": random.uniform(100, 500)
        })

    @task
    def query_database(self):
        self.client.post("/api/db/read", headers=self.headers, json={
            "query": "SELECT 1",
            "params": []
        })
