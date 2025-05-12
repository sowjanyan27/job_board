Feature: Item creation

  Scenario: Create an item successfully
    Given I have the following item details
    When I send a POST request to "/items/" with the item details
    Then the response status code should be 200
    And the response body should contain the item details
