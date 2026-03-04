import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Settings
from src.mcp_server import create_mcp_server
from src.routes import router


class HealthFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return "/healthy" not in msg and "/liveness" not in msg


def init_web_server(config: Settings) -> FastAPI:
    if config.APM_INSTRUMENTATION:
        try:
            from ddtrace import patch_all

            patch_all()
        except ImportError:
            pass

    app = FastAPI(
        title=config.DD_SERVICE,
        version=config.DD_VERSION,
        root_path=config.PREFIX_PATH,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Filter health check logs
    logging.getLogger("uvicorn.access").addFilter(HealthFilter())

    app.include_router(router)

    # Mount MCP SSE
    mcp = create_mcp_server(config)
    app.mount("/mcp", mcp.sse_app())

    return app
