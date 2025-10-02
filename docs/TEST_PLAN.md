# Test Plan – Fake Store API: Users

## 1. Introduction

This test plan describes the strategy, scope, and approach for testing the **Users** endpoints of the [Fake Store API](https://fakestoreapi.com/docs#tag/Users).  
Although this API is a mock service with limited validation, the tests are designed to reflect **production‑grade quality standards**.

---

## 2. Scope

- **Endpoints covered:**
  - `GET /users` – Retrieve all users
  - `GET /users/{id}` – Retrieve a single user by ID
  - `POST /users` – Create a new user
  - `PUT /users/{id}` – Update existing user
  - `DELETE /users/{id}` – Delete user by ID  

- **Out of scope:**
  - Endpoints outside the **Users** tag
  - Authentication / token‑based flows (not provided by API)

---

## 3. References

- [Fake Store API – Users Endpoints](https://fakestoreapi.com/docs#tag/Users)

---

## 4. Test Objectives

- Validate the correctness of response codes and payloads.
- Validate that API responses comply with the documented contract.
- Simulate production‑level validation even though the API does not enforce it.

---

## 5. Known Limitations

This API behaves as a **mock service**:

- No server‑side validation for required fields (`username`, `email`, `password`).
- Incorrect data types or malformed payloads often return `200` instead of error.
- Duplicate or invalid user data is accepted.

The tests will **simulate expected real‑world validations** to demonstrate proper test coverage and good practices.

---

## 6. Test Data

- **Positive data**: Valid `username`, `email`, `password`.
- **Negative data**: Missing fields, invalid types, malformed emails, invalid IDs.

## Validation Rules (Simulated)

These validations will be checked in tests even though API does not enforce them:

- **ID** 
  - must be integer. 
  - In creation request (POST), can be "id": 0 or omitted
  - In response, must be a positive integer
- **Username**
  - Must be a string
  - Length between 3 and 20 characters
  - Can contain only letters, digits, underscores (_)
    - Regex suggestion: ^[a-zA-Z0-9_]+$
  - Cannot be purely numeric (optional, if business rule applies)
- **Email**
  - Must match regex: `^[\w\.-]+@[\w\.-]+\.\w+$`
  - Must be unique (optional rule if system enforces it)
- **Password** 
  - Must be a string
  - Length: 8 to 64 characters
    - One uppercase letter
    - One lowercase letter
    - One digit
    - One special character (e.g., @, #, $, etc.)
- All required fields must be present in responses.

---

## 7. Test Scenarios

### 7.1. GET /users
- Verify response status code = `200`.
- Verify response body is a list of users.
- Verify each user object contains required keys:
  - `id` 
  - `username` 
  - `email` 
  - `password` 
  - `name.firstname` and `name.lastname`
  - `address.geolocation.lat` and `.long` as floats
  - Verify the total count of returned users > 0.
  - Verify uses have unique id.
  - Verify id not null.
  - Verify the total number of users with the number of records in DB.

### 7.2. GET /users/{id} 
- **Positive**
  - Verify status code = `200`.
  - Verify returned user matches the requested `id`.
  - Verify required fields and data types as above.
  - Verify User in DB.

- **Negative**
  - Invalid or non‑existent IDs should return error code (expected `400`).
  - Verify error response structure:
        - `status`
        - `message`

### 7.3. POST /users 
- **Positive**
  - Create a user with valid data and verify by ID.
  - Verify status code = `201`.
  - Verify response contains newly generated `id`.
  - Verify by subsequent `GET /users/{id}` that the user exists.
  - Verify user creation with min/max characters
  - Verify user data in DB.
  - Verify user ID is unique.
  - Verify permissions to Create User.

- **Negative**
  - Submit request with missing required fields (e.g., no `username`, `password`).
  - Submit invalid data types (e.g., string instead of integers, empty objects).
  - Use duplicated data (e.g., same username) and observe behavior.
  - Submit overly long strings in fields (e.g., `username` > 20 chars).
  - Submit invalid email format (e.g., `email="abc"`).
  - Submit unexpected fields and verify they are ignored or raise an error.
  - Submit with empty body and expect `4xx` error.

### 7.4. PUT /users/{id}
- **Positive**
  - Update an existing user with valid fields.
  - Verify status code = `200 OK`.
  - Verify updated fields are reflected in `GET /users/{id}`.
  - Update only specific fields and ensure other fields remain unchanged.
  - Verify updated fields in DB.
  - Verify permissions to Update User data.

- **Negative** 
  - Update non-existent user ID -> expect `4xx` error.
  - Send empty request body -> expect validation error or unchanged data.
  - Use invalid/malformed ID (e.g., negative, string) → expect `4xx` error.
  - Use invalid data types in the request body (e.g., integer instead of string).
  - Send null/blank values for required fields.
  
### 7.5. DELETE /users/{id}
- **Positive**
  - Delete an existing user by ID.
  - Verify status code = `200 OK`.
  - Verify deleted user id `GET /users/{id}` returns error or empty result.
  - Verify record was deleted in DB from all related tables.
  - Verify permissions to Delete User.
  
- **Negative**
  - Delete already deleted or non-existent user ID → expect `4xx` error.
  - Use invalid ID format (e.g., `null`, string) → expect error.
  - Try deleting without proper authorization (if applicable).

---


## 9. Deliverables

- **Feature files** under `features/` folder.
- **Step definitions** under `features/steps/` folder.
- Test data payloads under `payloads/` folder.
- This test plan (`docs/TEST_PLAN.md`).

---

## 10. Risks

- Since the API is fake, certain negative scenarios may pass (200 instead of 400).
- Test expectations may need adjustment if API behavior changes.

---

## 11. Conclusion

Even though the API is a mock service, this test plan implements a **real‑world API testing approach** with comprehensive CRUD coverage, contract validation, and simulated field validation.
