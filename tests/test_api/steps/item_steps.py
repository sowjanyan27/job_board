import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, when, then, parsers
from app.main import app

client = TestClient(app)

@pytest.fixture
def item_details():
    return {"name": "Apple", "price": 1.3}

@pytest.fixture
def response(item_details):
    """This fixture performs the POST request and returns the response."""
    return client.post("/items/", json=item_details)

@given("I have the following item details")
def given_item_details(item_details):
    return item_details

@when('I send a POST request to "/items/" with the item details')
def when_send_post(response):  # The step gets the response via the fixture
    pass  # Step required to match scenario; response will be used via fixture

@then("the response status code should be 200")
def then_status_code(response):
    assert response.status_code == 200

@then("the response body should contain the item details")
def then_response_body(response, item_details):
    data = response.json()
    assert data["name"] == item_details["name"]
    assert data["price"] == item_details["price"]
