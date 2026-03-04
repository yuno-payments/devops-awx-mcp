
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestHealthRoutes:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data

    def test_healthy(self, client):
        response = client.get("/healthy")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
        assert "environment" in data

    def test_liveness(self, client):
        response = client.get("/liveness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
