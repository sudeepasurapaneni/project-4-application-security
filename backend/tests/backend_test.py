import os
import pytest
import requests

BASE_URL = os.environ.get("WEBGUARD_API_URL", "http://127.0.0.1:5000").rstrip("/")


@pytest.fixture
def client():
    return requests.Session()


def test_health(client):
    response = client.get(f"{BASE_URL}/api/", timeout=15)
    assert response.status_code == 200
    assert response.json() == {"message": "WebGuard API is ready"}


def test_invalid_url(client):
    response = client.post(f"{BASE_URL}/api/scan", json={"url": "hello"}, timeout=15)
    assert response.status_code == 400
    assert response.json()["error"] == "Please enter a valid HTTP or HTTPS URL."


def test_missing_url(client):
    response = client.post(f"{BASE_URL}/api/scan", json={}, timeout=15)
    assert response.status_code == 400
    assert "valid HTTP or HTTPS URL" in response.json()["error"]


def test_real_scan_example_com(client):
    response = client.post(f"{BASE_URL}/api/scan", json={"url": "https://example.com"}, timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert len(data["headers"]) == 5
    assert {item["name"] for item in data["headers"]} == {
        "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options",
        "X-Frame-Options", "Referrer-Policy",
    }
    assert data["issues_found"] == sum(not item["present"] for item in data["headers"])
    assert data["final_url"].startswith("https://")


def test_unreachable_site(client):
    response = client.post(f"{BASE_URL}/api/scan", json={"url": "http://nonexistent.invalid"}, timeout=30)
    assert response.status_code == 422
    assert response.json()["error"].startswith("Request failed:")
