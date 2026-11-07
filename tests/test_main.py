
from fastapi.testclient import TestClient

from fast import app, r

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FastAPI running"


def test_me():
    response = client.get("/me")
    assert response.status_code == 200
    assert response.json()["name"] == "Neeraj"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_redis_connection():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["redis"] == "connected"


def test_redis_write_read():
    response = client.get("/redis-test")

    assert response.status_code == 200
    assert response.json()["redis_value"] == "connected"

    assert r.get("my_key") == "Hello from Redis! Welcome to my world!"
