from pytest_bdd import scenario, given, when, then

@scenario('features/simple_test.feature', 'Always passes')
def test_always_passes():
    pass

@given('the system is working')
def system_is_working():
    pass

@when('I run the test')
def run_the_test():
    pass

@then('it should pass')
def it_should_pass():
    assert True
