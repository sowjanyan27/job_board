"""
created_by: sowjanya
created_date:08-05-2025
modified_date:09-05-2025
Description:This test file uses httpx.AsyncClient
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import your FastAPI application
from app.core.logger import get_logger  # Import the logger setup

# Get a logger instance for the test module
logger = get_logger("test_users", log_file="log/test_users.log")
# This test file uses httpx.AsyncClient with ASGITransport to test FastAPI endpoints asynchronously.
# It avoids starting a real HTTP server by sending requests directly to the ASGI app in memory.

# Mark the test as asynchronous so pytest-asyncio can handle it


# This test file uses httpx.AsyncClient with ASGITransport to test FastAPI endpoints asynchronously.
@pytest.mark.asyncio
async def test_get_users_async():
    logger.info("Starting test_get_users_async")

    # Create an ASGITransport to allow httpx to call the FastAPI app directly in memory
    transport = ASGITransport(app=app)

    # Use AsyncClient to send async HTTP requests
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Send a GET request to the /users endpoint with valid query parameters
        response = await client.get("/users/?skip=0&limit=10000")

        # Ensure the response returns HTTP 200 OK
        assert response.status_code == 200

        # Parse the JSON response body
        data = response.json()

        # Check that the response is a list (expected from /users endpoint)
        assert isinstance(data, list)

        # Optional: Check that at least one user exists and the first user's name is 'User_1'
        if data:
            assert "name" in data[0]  # Ensure 'name' key exists in the first user object
            assert data[0]["name"] == "User_1"  # Check that the name matches expected static value
            logger.info("First user name verified successfully.")
        else:
            # If the list is empty, skip the test (useful in unseeded environments)
            logger.warning("No users returned, skipping test.")
            pytest.skip("No users returned")

    logger.info("test_get_users_async completed.")

# Another asynchronous test for invalid query parameters
@pytest.mark.asyncio
async def test_get_users_invalid_params_async():
    logger.info("Starting test_get_users_invalid_params_async")

    # Set up the same ASGI in-memory transport
    transport = ASGITransport(app=app)

    # Create an AsyncClient for sending requests
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Pass invalid query parameters: negative skip and limit
        response = await client.get("/users/?skip=-1&limit=-5")

        # FastAPI should return a 422 Unprocessable Entity due to Pydantic validation
        assert response.status_code == 422

        # Ensure the response contains a 'detail' key which describes the validation errors
        assert "detail" in response.json()

    logger.info("test_get_users_invalid_params_async completed.")
