from unittest.mock import MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from src.services.base_service import BaseCRUDService
from src.tools.inventories import register_inventory_tools


@pytest.fixture
def setup():
    mcp = FastMCP("test")
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    service = BaseCRUDService(client, "/api/v2/inventories/")
    register_inventory_tools(mcp, service)
    return mcp, client, service


class TestInventoryTools:
    def test_tools_registered(self, setup):
        mcp, _, _ = setup
        tool_names = [t.name for t in mcp._tool_manager.list_tools()]
        assert "list_inventories" in tool_names
        assert "get_inventory" in tool_names
        assert "create_inventory" in tool_names
        assert "update_inventory" in tool_names
        assert "delete_inventory" in tool_names

    def test_list_inventories(self, setup):
        _, client, _ = setup
        client.request.return_value = {
            "count": 1,
            "results": [{"id": 1, "name": "Default"}],
            "next": None,
        }

        # Get the tool function directly
        from src.tools.inventories import register_inventory_tools
        mcp2 = FastMCP("test2")
        client2 = MagicMock()
        client2.__enter__ = MagicMock(return_value=client2)
        client2.__exit__ = MagicMock(return_value=False)
        client2.request.return_value = {
            "count": 1,
            "results": [{"id": 1, "name": "Default"}],
            "next": None,
        }
        service2 = BaseCRUDService(client2, "/api/v2/inventories/")
        register_inventory_tools(mcp2, service2)

        # Find and call the tool
        tools = {t.name: t for t in mcp2._tool_manager.list_tools()}
        assert "list_inventories" in tools
