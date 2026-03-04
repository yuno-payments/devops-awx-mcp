from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from client.ansible_client import AnsibleClient
from config import Settings


@pytest.fixture
def mock_config():
    return Settings(
        ANSIBLE_BASE_URL="https://awx.test.local",
        ANSIBLE_TOKEN="test-token-123",
        ANSIBLE_VERIFY_SSL=False,
        ANSIBLE_TIMEOUT=5,
        SERVER_MODE="single-worker",
        DD_ENV="test",
    )


@pytest.fixture
def mock_ansible_client(mock_config):
    client = AnsibleClient(mock_config)
    client.token = "test-token-123"
    client.session = MagicMock()
    return client


@pytest.fixture
def mock_response():
    def _make_response(status_code=200, json_data=None, text=""):
        resp = MagicMock()
        resp.status_code = status_code
        resp.text = text or (str(json_data) if json_data else "")
        resp.json.return_value = json_data or {}
        resp.headers = {"Content-Type": "application/json"}
        resp.cookies = {}
        return resp
    return _make_response


@pytest.fixture
def test_app(mock_config):
    with patch("web_server.create_mcp_server") as mock_mcp:
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.sse_app.return_value = MagicMock()
        mock_mcp.return_value = mock_mcp_instance

        from web_server import init_web_server
        app = init_web_server(mock_config)
        return TestClient(app)
