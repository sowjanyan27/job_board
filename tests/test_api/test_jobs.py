# tests/test_api/test_jobs.py

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

# assert is a statement used for debugging and testing(assert is used to validate that the expected outcomes occur during the test)
# Fixture to provide the TestClient to use in each test function
# The fixture is scoped to the "module", meaning it is set up once per module (faster)
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:  # Initialize the TestClient with the FastAPI app
        yield client  # Return the client instance to be used in tests


# Test for retrieving jobs with valid parameters
def test_get_jobs(test_client):
    # Send GET request to the /jobs endpoint with valid query parameters
    response = test_client.get("/jobs/?skip=0&limit=10000")

    # Ensure the response status code is 200 OK, meaning the request was successful
    assert response.status_code == 200

    # Assert that the response body is a list of jobs
    assert isinstance(response.json(), list)

    # Additional check can be added if expected jobs exist in the response data
    # Example: assert len(response.json()) > 0, "Expected jobs to be returned"


# Test for retrieving jobs with invalid query parameters (negative skip and limit)
def test_get_jobs_invalid_params(test_client):
    # Send GET request to the /jobs endpoint with invalid parameters (negative skip and limit)
    response = test_client.get("/jobs/?skip=-1&limit=-5")

    # Ensure that FastAPI returns 422 status code, meaning the parameters couldn't be processed
    assert response.status_code == 422

    # Check that the response body contains the 'detail' key, which holds error messages for invalid inputs
    assert "detail" in response.json(), "'detail' key should be present in the error response"

def test_fetch_jobs_with_filters(test_client):
    # Test with valid filters
    response = test_client.get("/jobs/filter?skip=ABC&limit=ABC")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
    assert len(data) <= 10  # Check that the number of jobs does not exceed the limit

    # Test with cache hit by sending the same request again
    response2 = test_client.get("/jobs/filter?company=ABC&skip=0&limit=10")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data == data2  # Ensure the response data is the same (cache hit)


def test_fetch_jobs_with_types(test_client):
    # Test with valid filters
    response = test_client.get("/jobs/?skip=abc&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure it's a list of jobs
    # assert len(data) <= 10  # Check that the number of jobs does not exceed the limit
