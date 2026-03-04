import pytest
from starlette.testclient import TestClient

from config import Settings
from mcp_server import create_mcp_server


@pytest.fixture
def client():
    config = Settings(
        ANSIBLE_BASE_URL="https://awx.test.local",
        ANSIBLE_TOKEN="test-token",
        ANSIBLE_VERIFY_SSL=False,
        PREFIX_PATH="/devops-awx-mcp",
    )
    mcp = create_mcp_server(config)
    app = mcp.streamable_http_app()
    return TestClient(app)


class TestHealthRoutes:
    def test_root(self, client):
        response = client.get("/devops-awx-mcp/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data

    def test_healthy(self, client):
        response = client.get("/devops-awx-mcp/healthy")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
        assert "environment" in data

    def test_liveness(self, client):
        response = client.get("/devops-awx-mcp/liveness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
