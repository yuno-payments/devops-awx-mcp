from unittest.mock import MagicMock, call

from src.client.pagination import handle_pagination


class TestHandlePagination:
    def test_single_page(self):
        client = MagicMock()
        client.request.return_value = {
            "count": 2,
            "results": [{"id": 1}, {"id": 2}],
            "next": None,
        }

        results = handle_pagination(client, "/api/v2/inventories/", {"limit": 100})
        assert len(results) == 2
        assert results[0]["id"] == 1

    def test_multiple_pages(self):
        client = MagicMock()
        client.request.side_effect = [
            {
                "count": 4,
                "results": [{"id": 1}, {"id": 2}],
                "next": "/api/v2/inventories/?page=2",
            },
            {
                "count": 4,
                "results": [{"id": 3}, {"id": 4}],
                "next": None,
            },
        ]

        results = handle_pagination(client, "/api/v2/inventories/", {"limit": 2})
        assert len(results) == 4

    def test_non_paginated_response(self):
        client = MagicMock()
        client.request.return_value = {"id": 1, "name": "single"}

        results = handle_pagination(client, "/api/v2/inventories/1/")
        assert len(results) == 1
        assert results[0]["id"] == 1

    def test_empty_results(self):
        client = MagicMock()
        client.request.return_value = {
            "count": 0,
            "results": [],
            "next": None,
        }

        results = handle_pagination(client, "/api/v2/inventories/")
        assert results == []

    def test_params_cleared_after_first_page(self):
        client = MagicMock()
        client.request.side_effect = [
            {"count": 2, "results": [{"id": 1}], "next": "/api/v2/inventories/?page=2"},
            {"count": 2, "results": [{"id": 2}], "next": None},
        ]

        handle_pagination(client, "/api/v2/inventories/", {"limit": 1})

        # Second call should have params=None
        assert client.request.call_args_list[1] == call("GET", "/api/v2/inventories/?page=2", params=None)
