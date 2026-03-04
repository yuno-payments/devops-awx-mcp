import json
import re

import requests

from src.config import Settings


class AnsibleClient:
    def __init__(self, config: Settings):
        self.base_url = config.ANSIBLE_BASE_URL.rstrip("/")
        self.username = config.ANSIBLE_USERNAME
        self.password = config.ANSIBLE_PASSWORD
        self.token = config.ANSIBLE_TOKEN
        self.verify_ssl = config.ANSIBLE_VERIFY_SSL
        self.timeout = config.ANSIBLE_TIMEOUT
        self.session = requests.Session()
        self.session.verify = self.verify_ssl

    def __enter__(self):
        if not self.token and self.username and self.password:
            self._authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Keep session alive for reuse

    def close(self):
        self.session.close()

    def _authenticate(self) -> str:
        login_page = self.session.get(
            f"{self.base_url}/api/login/",
            timeout=self.timeout,
        )

        csrf_token = None
        if "csrftoken" in login_page.cookies:
            csrf_token = login_page.cookies["csrftoken"]
        else:
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
            if match:
                csrf_token = match.group(1)

        if not csrf_token:
            raise Exception("Could not obtain CSRF token")

        headers = {
            "Referer": f"{self.base_url}/api/login/",
            "X-CSRFToken": csrf_token,
        }

        login_data = {
            "username": self.username,
            "password": self.password,
            "next": "/api/v2/",
        }

        login_response = self.session.post(
            f"{self.base_url}/api/login/",
            data=login_data,
            headers=headers,
            timeout=self.timeout,
        )

        if login_response.status_code >= 400:
            raise Exception(f"Login failed: {login_response.status_code} - {login_response.text}")

        token_headers = {
            "Content-Type": "application/json",
            "Referer": f"{self.base_url}/api/v2/",
        }

        if "csrftoken" in self.session.cookies:
            token_headers["X-CSRFToken"] = self.session.cookies["csrftoken"]

        token_data = {
            "description": "MCP Server Token",
            "application": None,
            "scope": "write",
        }

        token_response = self.session.post(
            f"{self.base_url}/api/v2/tokens/",
            json=token_data,
            headers=token_headers,
            timeout=self.timeout,
        )

        if token_response.status_code == 201:
            data = token_response.json()
            self.token = data.get("token")
            return self.token
        else:
            raise Exception(f"Token creation failed: {token_response.status_code} - {token_response.text}")

    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}" if endpoint.startswith("/") else endpoint
        headers = self._get_headers()

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            raise Exception(f"Ansible API error: {response.status_code} - {response.text}")

        if response.status_code == 204:
            return {"status": "success"}

        if not response.text.strip():
            return {"status": "success", "message": "Empty response"}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "status": "success",
                "content_type": response.headers.get("Content-Type", "unknown"),
                "text": response.text[:1000],
            }

    def raw_get(self, url: str) -> requests.Response:
        return self.session.get(url, headers=self._get_headers(), timeout=self.timeout)
