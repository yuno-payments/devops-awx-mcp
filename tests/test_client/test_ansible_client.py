import json
from unittest.mock import MagicMock

import pytest

from client.ansible_client import AnsibleClient
from config import Settings


@pytest.fixture
def config():
    return Settings(
        ANSIBLE_BASE_URL="https://awx.test.local",
        ANSIBLE_USERNAME="admin",
        ANSIBLE_PASSWORD="password123",
        ANSIBLE_VERIFY_SSL=False,
        ANSIBLE_TIMEOUT=5,
    )


@pytest.fixture
def token_config():
    return Settings(
        ANSIBLE_BASE_URL="https://awx.test.local",
        ANSIBLE_TOKEN="pre-existing-token",
        ANSIBLE_VERIFY_SSL=False,
    )


class TestAnsibleClientInit:
    def test_creates_session(self, config):
        client = AnsibleClient(config)
        assert client.base_url == "https://awx.test.local"
        assert client.username == "admin"
        assert client.verify_ssl is False
        assert client.session is not None

    def test_strips_trailing_slash(self):
        cfg = Settings(ANSIBLE_BASE_URL="https://awx.test.local/")
        client = AnsibleClient(cfg)
        assert client.base_url == "https://awx.test.local"


class TestAnsibleClientContextManager:
    def test_enter_with_token_skips_auth(self, token_config):
        client = AnsibleClient(token_config)
        with client:
            assert client.token == "pre-existing-token"

    def test_enter_without_credentials_skips_auth(self):
        cfg = Settings(ANSIBLE_BASE_URL="https://awx.test.local")
        client = AnsibleClient(cfg)
        with client:
            assert client.token == ""


class TestAnsibleClientRequest:
    def test_successful_json_response(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"id": 1, "name": "test"}'
        mock_resp.json.return_value = {"id": 1, "name": "test"}
        mock_resp.headers = {"Content-Type": "application/json"}
        client.session = MagicMock()
        client.session.request.return_value = mock_resp

        result = client.request("GET", "/api/v2/inventories/1/")
        assert result == {"id": 1, "name": "test"}

    def test_204_no_content(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        mock_resp.status_code = 204
        client.session = MagicMock()
        client.session.request.return_value = mock_resp

        result = client.request("DELETE", "/api/v2/inventories/1/")
        assert result == {"status": "success"}

    def test_error_response_raises(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = "Not Found"
        client.session = MagicMock()
        client.session.request.return_value = mock_resp

        with pytest.raises(Exception, match="Ansible API error: 404"):
            client.request("GET", "/api/v2/inventories/999/")

    def test_empty_response(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "  "
        client.session = MagicMock()
        client.session.request.return_value = mock_resp

        result = client.request("POST", "/api/v2/test/")
        assert result["status"] == "success"

    def test_non_json_response(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "plain text response"
        mock_resp.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_resp.headers = {"Content-Type": "text/plain"}
        client.session = MagicMock()
        client.session.request.return_value = mock_resp

        result = client.request("GET", "/api/v2/metrics/")
        assert result["status"] == "success"
        assert result["content_type"] == "text/plain"

    def test_headers_include_bearer_token(self, token_config):
        client = AnsibleClient(token_config)
        headers = client._get_headers()
        assert headers["Authorization"] == "Bearer pre-existing-token"
        assert headers["Content-Type"] == "application/json"

    def test_raw_get(self, token_config):
        client = AnsibleClient(token_config)
        mock_resp = MagicMock()
        client.session = MagicMock()
        client.session.get.return_value = mock_resp

        result = client.raw_get("https://awx.test.local/api/v2/jobs/1/stdout/?format=txt")
        assert result == mock_resp
