import pytest
import requests
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app  # Assuming app is the FastAPI instance

# # Synchronous TestClient Fixture
@pytest.fixture(scope="module")
def test_client():
    """Fixture to provide the TestClient for FastAPI tests."""
    with TestClient(app) as client:  # Initialize the TestClient with the FastAPI app
        yield client  # Return the client instance to be used in tests

@pytest.fixture
def send_get_request(test_client, user_query_parameters):
    """Fixture to send a GET request with query parameters."""
    response = test_client.get("/users", params=user_query_parameters)
    return response

