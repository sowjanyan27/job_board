# tests/test_api/test_users.py

import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import FastAPI app

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def test_get_users(test_client):
    response = test_client.get("/users/?skip=0&limit=10000")  # Make GET request
    assert response.status_code == 200  # Check for 200 OK response
    assert isinstance(response.json(), list)  # Ensure the response is a list
