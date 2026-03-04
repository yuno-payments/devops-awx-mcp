import sys

from config import load_config


def main():
    config = load_config()

    if config.SERVER_MODE == "stdio":
        from mcp_server import create_mcp_server

        mcp = create_mcp_server(config)
        mcp.run(transport="stdio")
        sys.exit(0)

    from web_server import init_web_server

    return init_web_server(config)


if __name__ == "__main__":
    import uvicorn

    config = load_config()
    if config.SERVER_MODE == "stdio":
        main()
    else:
        workers = 1 if config.SERVER_MODE == "single-worker" else 1  # SSE needs single worker
        reload = config.SERVER_MODE == "single-worker"
        uvicorn.run(
            "main:main",
            host=config.HOST,
            port=config.PORT,
            workers=workers,
            factory=True,
            reload=reload,
        )
