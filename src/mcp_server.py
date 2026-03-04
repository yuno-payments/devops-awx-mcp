from mcp.server.fastmcp import FastMCP

from config import Settings

mcp = FastMCP("devops-awx-mcp")


def create_mcp_server(config: Settings) -> FastMCP:
    from tools import register_all_tools

    register_all_tools(mcp, config)
    return mcp
