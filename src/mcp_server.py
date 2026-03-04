from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import Settings


def create_mcp_server(config: Settings) -> FastMCP:
    mcp = FastMCP(
        "devops-awx-mcp",
        host=config.HOST,
        port=config.PORT,
        json_response=True,
    )

    # Register MCP tools
    from tools import register_all_tools

    register_all_tools(mcp, config)

    # Health check routes (same pattern as datadog-mcp)
    health_prefix = config.PREFIX_PATH.rstrip("/")

    @mcp.custom_route(f"{health_prefix}/healthy", methods=["GET"])
    async def healthy(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "status": "healthy",
                "service": config.DD_SERVICE,
                "version": config.DD_VERSION,
                "environment": config.DD_ENV,
            }
        )

    @mcp.custom_route(f"{health_prefix}/liveness", methods=["GET"])
    async def liveness(request: Request) -> JSONResponse:
        return JSONResponse({"status": "alive"})

    @mcp.custom_route(f"{health_prefix}/", methods=["GET"])
    async def root(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "service": config.DD_SERVICE,
                "version": config.DD_VERSION,
            }
        )

    return mcp
