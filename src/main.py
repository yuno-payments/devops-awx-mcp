import sys

from config import load_config


def main():
    config = load_config()
    from mcp_server import create_mcp_server

    mcp = create_mcp_server(config)

    if config.SERVER_MODE == "stdio":
        mcp.run(transport="stdio")
        sys.exit(0)

    # HTTP mode: Streamable HTTP (MCP spec 2025)
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
