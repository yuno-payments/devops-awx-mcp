from unittest.mock import MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from services.system_service import SystemService
from tools.system import register_system_tools


@pytest.fixture
def setup():
    mcp = FastMCP("test")
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    service = SystemService(client)
    register_system_tools(mcp, service)
    return mcp, client


class TestSystemTools:
    def test_tools_registered(self, setup):
        mcp, _ = setup
        tool_names = [t.name for t in mcp._tool_manager.list_tools()]
        assert "get_ansible_version" in tool_names
        assert "get_dashboard_stats" in tool_names
        assert "get_metrics" in tool_names
