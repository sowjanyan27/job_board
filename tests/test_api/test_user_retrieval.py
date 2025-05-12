import pytest
from pytest_bdd import scenario, given, when, then
from fastapi.testclient import TestClient
from app.main import app

# Fixture for sending a GET request
@pytest.fixture
def send_get_request(test_client, user_query_parameters):
    """Fixture to send a GET request with query parameters."""
    response = test_client.get("/users", params=user_query_parameters)
    return response

# Fixture to provide the TestClient for FastAPI tests
@pytest.fixture(scope="module")
def test_client():
    """Fixture to provide the TestClient for FastAPI tests."""
    with TestClient(app) as client:
        yield client

# Setup Query Parameters Fixture with a unique name
@pytest.fixture(scope="function")
def user_query_parameters():
    """Fixture to set up query parameters."""
    return {"skip": 0, "limit": 10}

# Scenario for BDD
@scenario('features/user_retrieval.feature', 'Get users with valid query parameters')
def test_get_users():
    pass

# Step Definitions

# Given step
@given('the user accesses the /users endpoint with valid query parameters "skip=0" and "limit=10"')
def setup_query_parameters(user_query_parameters):
    return user_query_parameters

# When step
@when('the user sends a GET request to the /users endpoint')
def send_get_request(test_client, user_query_parameters):
    """Sends a GET request to the /users endpoint with query parameters."""
    response = test_client.get("/users", params=user_query_parameters)
    return response

# Then steps
@then('the response status code should be 200')
def check_status_code(send_get_request):
    response = send_get_request
    print("Response Content:",response.text)
    assert response.status_code == 200

@then('the response should contain 10 users')
def check_response_data(send_get_request):
    response = send_get_request
    assert len(response.json()) == 10
