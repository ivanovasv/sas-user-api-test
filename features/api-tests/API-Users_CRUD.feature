Feature: API: Users CRUD

  Scenario: API: Users CRUD (Mock)
    # Create new user
    * API: Prepare payload for create_user.json
      | jsonPath   | value               |
      | $.username | test_user           |
      | $.email    | test_user@gmail.com |
      | $.password | tesT!78             |

    * API: Send POST /users request with payload
    * API: response should have api status code 201

    # Verify user by id - mocked data
    * API: Send GET /users/10 request without payload
    * API: response should have api status code 200

    * API: Response should have values
      | jsonPath         | value            |
      | $.username       | jimmie_k         |
      | $.email          | jimmie@gmail.com |
      | $.password       | klein*#%*        |
      | $.name.firstname | jimmie           |
      | $.name.lastname  | klein            |

    # Update user
    * API: Prepare payload for update_user.json
      | jsonPath   | value            |
      | $.id       | 10               |
      | $.username | jimmie_k         |
      | $.email    | jimmie@gmail.com |
      | $.password | tesT!78          |

    * API: Send PUT /users/10 request with payload
    * API: response should have api status code 200

    # Delete user
    * API: Send DELETE /users/10 request without payload
    * API: response should have api status code 200

    # Verify deleted user id returns error or empty response - mock data
    * API: Send GET /users/12 request without payload
    * API: response should have api status code 200

    * API: Response should not have values
      | jsonPath | value |
      | $.id     | 12    |