import requests
from common.payload_builder import *


class ApiClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }

        # Add Authorization header if token is provided
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def send_request(self, method, endpoint, payload=None):
        full_url = f"{self.base_url}{endpoint}"

        print("\n" + "=" * 40)
        print(f"{method.upper()} → {full_url}")
        print(f"Payload: {json.dumps(payload) if payload else 'None'}")

        # Send the request
        response = requests.request(
            method=method.upper(),
            url=full_url,
            headers=self.headers,
            json=payload
        )

        print(f"Status Code: {response.status_code}")

        # Try parsing the response as JSON; fallback to plain text
        try:
            parsed = response.json()
            print("Response:", json.dumps(parsed))
        except ValueError:
            print("Raw Response:", response.text)

        print("=" * 40 + "\n")
        return response
