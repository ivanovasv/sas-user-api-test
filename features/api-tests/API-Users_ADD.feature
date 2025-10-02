Feature: API: Users ADD

  # API contract: https://fakestoreapi.com/docs#tag/Users/operation/addUser

  Scenario Outline: API: Add new user and verify by ID - positive
    * API: Prepare payload for create_user.json
      | jsonPath   | value                 |
      | $.username | test_user_1           |
      | $.email    | test_user_1@gmail.com |
      | $.password | testUser1!            |
    * API: Send POST /users request with payload
    * API: response should have api status code 201
    * API: Save values from JSON response
      | jsonPath | varName |
      | $.id     | user_id |

    # Verify user was created with correct data
    * API: Send GET /users/context.user_id request without payload
    * API: response should have api status code 200
    * API: Response should have values
      | jsonPath   | value           |
      | $.id       | context.user_id |
      | $.email    | <email>         |
      | $.username | <username>      |
      | $.password | <password>      |

    Examples:
      | email                 | username    | password   |
      | test_user_1@gmail.com | test_user_1 | testUser1! |

  Scenario Outline: API: Add new user with minimum/maximum chars in required fields - positive
    * API: Prepare payload for create_user.json
      | jsonPath   | value          |
      | $.username | <username>     |
      | $.email    | user@gmail.com |
      | $.password | <password>     |
    * API: Send POST /users request with payload
    * API: response should have api status code 201

    Examples:
      | username             | password                                                         |
      | min_user             | MinPas!1                                                         |
      | thisusernamemaxchars | thisisthemaximumpassword1$Thisismaximumpassword321#hellopassword |

  Scenario: API: Create new user without payload - negative
    * API: Send POST /users request without payload
    * API: response should have api status code 400

  Scenario Outline: API: Create user with invalid ID data types - negative
    * API: Prepare payload for create_user.json
      | jsonPath   | value               |
      | $.id       | <id>                |
      | $.username | test_user_2         |
      | $.email    | test_user@gmail.com |
      | $.password | tesT!78             |
    * API: Send POST /users request with payload
    * API: response should have api status code 400

    Examples:
      | id   |
      | test |
      | null |
      | O    |
      | !    |

  Scenario Outline: API: Add user with invalid username - negative
    * API: Prepare payload for create_user.json
      | jsonPath   | value              |
      | $.username | <username>         |
      | $.email    | test_user@mail.com |
      | $.password | ValidP@ss1         |
    * API: Send POST /users request with payload
    * API: response should have api status code 400

    Examples:
      | username              |
      | ab                    |
      | a                     |
      | thisistoolongusername |
      | !@#                   |
      |                       |

  Scenario Outline: API: Create user with invalid email - negative
    * API: Prepare payload for create_user.json
      | jsonPath   | value       |
      | $.username | test_user_3 |
      | $.email    | <email>     |
      | $.password | tesT!123    |
    * API: Send POST /users request with payload
    * API: response should have api status code 400

    Examples:
      | email           |
      | no_at_gmail.com |
      | user@gmail      |
      | @gmail.com      |
      | user@.com       |
      |                 |

  Scenario Outline: API: Create user with invalid password - negative
    * API: Prepare payload for create_user.json
      | jsonPath   | value          |
      | $.username | test_user_4    |
      | $.email    | weak@gmail.com |
      | $.password | <password>     |
    * API: Send POST /users request with payload
    * API: response should have api status code 400

    Examples:
      | password     |
      | short        |
      | noDigits!    |
      | NOLOWERS123! |
      | noupper123!  |
      | noSpecial123 |
      |              |

  Scenario: API: Add new user with unexpected fields - negative
    * API: Prepare payload for create_user.json
      | jsonPath   | value              |
      | $.username | test_user_5        |
      | $.email    | testuser@gmail.com |
      | $.password | testUser123$       |
      | $.nickname | qa_test            |
    * API: Send POST /users request with payload
    * API: response should have api status code 400