from unittest.mock import MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from services.job_service import JobService
from tools.jobs import register_job_tools


@pytest.fixture
def setup():
    mcp = FastMCP("test")
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    service = JobService(client)
    register_job_tools(mcp, service)
    return mcp, client


class TestJobTools:
    def test_tools_registered(self, setup):
        mcp, _ = setup
        tool_names = [t.name for t in mcp._tool_manager.list_tools()]
        assert "list_jobs" in tool_names
        assert "get_job" in tool_names
        assert "cancel_job" in tool_names
        assert "get_job_events" in tool_names
        assert "get_job_stdout" in tool_names
