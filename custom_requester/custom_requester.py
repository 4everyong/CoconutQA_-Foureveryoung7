from constants import BASE_URL
import requests

class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()

    def send_request(self, method, endpoint, data=None, expected_status=200):
        url = f"{BASE_URL}{endpoint}"
        response = self.session.request(method, url, json=data, headers=self.headers)
        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status: {response.status_code}, expected_status: {expected_status}")
        return response