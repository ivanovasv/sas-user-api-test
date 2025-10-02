Feature: API: Users GET

  """
    API contract GET all users: https://fakestoreapi.com/docs#tag/Users/operation/getAllUsers
    API contract GET user by ID: https://fakestoreapi.com/docs#tag/Users/operation/getUserById
  """

  Scenario: API: Get all users
    * API: Send GET /users request without payload
    * API: response should have api status code 200

  Scenario Outline: API: Get user by ID - positive
    * API: Send GET /users/<id> request without payload
    * API: response should have api status code 200
    * API: Response should have values
      | jsonPath   | value      |
      | $.id       | <id>       |
      | $.email    | <email>    |
      | $.username | <username> |
      | $.password | <password> |

    Examples:
      | id | email          | username | password |
      | 1  | john@gmail.com | johnd    | m38rmF$  |

  Scenario: API: Validate structure of user object in users list
    * API: Send GET /users request without payload
    * API: response should have api status code 200
    * API: Response should have values
      | jsonPath                     | value          |
      | $[0].id                      | 1              |
      | $[0].email                   | john@gmail.com |
      | $[0].username                | johnd          |
      | $[0].password                | m38rmF$        |
      | $[0].name.firstname          | john           |
      | $[0].name.lastname           | doe            |
      | $[0].address.city            | kilcoole       |
      | $[0].address.geolocation.lat | -37.3159       |

  Scenario Outline: API: Get user by incorrect ID - negative
    * API: Send GET /users/<id> request without payload
    * API: response should have api status code 400
    * API: Response should have values
      | jsonPath  | value                      |
      | $.status  | error                      |
      | $.message | user id should be provided |

    Examples:
      | id   |
      | -1   |
      | 0    |
      | null |
      | abc  |