# 🧪 User API Test Automation (Behave + Python)

This project contains API test scenarios for the [Fake Store API](https://fakestoreapi.com/docs#tag/Users), focused on the `/users` endpoint.  
It uses **Python**, **Behave**, and **requests** to cover CRUD operations with reusable steps and payloads.

---

## 📂 Project Structure

### `common/` – Reusable Python helpers
- `api_client.py` – HTTP client logic (GET, POST, PUT, DELETE)
- `payload_builder.py` – Payload preparation and updates
- `utils.py` – Utility functions (e.g., context value resolution)

### `docs/` – Documentation
- `test_plan.md` – Manual test plan for the `/users` endpoint

### `features/` – Behave feature files and steps
- `environment.py` – Behave environment configuration

#### `features/api-tests/` – Gherkin test scenarios
- `API-Users_ADD.feature`
- `API-Users_CRUD.feature`
- `API-Users_GET.feature`

#### `features/steps/` – Step definitions and setup
- `api_steps.py` – Step implementations

### `payloads/` – JSON request bodies
- `create_user.json`
- `update_user.json`

### Root files
- `requirements.txt` – Python dependencies
- `README.md` – Project overview (this file)

---

## 🚀 How to Run Tests

1. Install requirements:

```bash
pip install -r requirements.txt
