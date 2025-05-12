from pytest_bdd import scenario
from tests.test_api.steps.item_steps import *  # Import steps and fixtures

@scenario('features/item_creation.feature', 'Create an item successfully')
def test_create_an_item_successfully():
    pass
