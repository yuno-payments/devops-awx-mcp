from unittest.mock import MagicMock

import pytest

from src.services.base_service import BaseCRUDService


@pytest.fixture
def service():
    client = MagicMock()
    return BaseCRUDService(client, "/api/v2/inventories/")


class TestBaseCRUDService:
    def test_list(self, service):
        service.client.request.return_value = {
            "count": 1,
            "results": [{"id": 1, "name": "test"}],
            "next": None,
        }

        results = service.list(limit=50, offset=0)
        assert len(results) == 1
        assert results[0]["name"] == "test"

    def test_get(self, service):
        service.client.request.return_value = {"id": 1, "name": "test"}

        result = service.get(1)
        assert result["id"] == 1
        service.client.request.assert_called_with("GET", "/api/v2/inventories/1/")

    def test_create(self, service):
        service.client.request.return_value = {"id": 1, "name": "new"}

        result = service.create({"name": "new", "organization": 1})
        assert result["name"] == "new"
        service.client.request.assert_called_with("POST", "/api/v2/inventories/", data={"name": "new", "organization": 1})

    def test_update(self, service):
        service.client.request.return_value = {"id": 1, "name": "updated"}

        result = service.update(1, {"name": "updated"})
        assert result["name"] == "updated"
        service.client.request.assert_called_with("PATCH", "/api/v2/inventories/1/", data={"name": "updated"})

    def test_delete(self, service):
        service.client.request.return_value = {"status": "success"}

        result = service.delete(1)
        assert result["status"] == "success"
        service.client.request.assert_called_with("DELETE", "/api/v2/inventories/1/")

    def test_list_with_filters(self, service):
        service.client.request.return_value = {
            "count": 1,
            "results": [{"id": 1}],
            "next": None,
        }

        service.list(limit=10, offset=0, status="active")
        call_args = service.client.request.call_args
        assert call_args[1]["params"]["status"] == "active"
