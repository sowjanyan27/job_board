Feature: User Retrieval

  Scenario: Get users with valid query parameters
    Given the user accesses the /users endpoint with valid query parameters "skip=0" and "limit=10"
    When the user sends a GET request to the /users endpoint
    Then the response status code should be 200
    And the response should contain 10 users

  Scenario: Get users with only the skip query parameter
    Given the user accesses the /users endpoint with the query parameter "skip=10"
    When the user sends a GET request to the /users endpoint
    Then the response status code should be 200
    And the response should contain users starting from the 11th user onward

  Scenario: Get users with both skip and limit query parameters
    Given the user accesses the /users endpoint with the query parameters "skip=5" and "limit=10"
    When the user sends a GET request to the /users endpoint
    Then the response status code should be 200
    And the response should contain 10 users starting from the 6th user onward
