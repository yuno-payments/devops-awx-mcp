# devops-awx-mcp

MCP Server for Ansible Tower/AWX with 72+ tools. Dual transport: stdio (local) + HTTP/SSE (Kingdom deploy).

## Stack
- Python 3.12, FastAPI, Pydantic Settings, MCP SDK (FastMCP)
- `requests` for AWX API, `ddtrace` for Datadog APM
- PDM for dependency management

## Architecture
```
Request → FastAPI (web_server.py) → MCP SSE mount (/mcp)
                                  → Health routes (/healthy, /liveness)

MCP Tool call → tools/<domain>.py → services/ → client/ansible_client.py → AWX API
```

### Layers
- **`src/config.py`** — Pydantic Settings (env vars)
- **`src/client/`** — AnsibleClient (auth, HTTP, session) + pagination
- **`src/services/`** — BaseCRUDService (generic CRUD) + specialized services
- **`src/tools/`** — MCP tool registration (14 modules, ~72 tools)
- **`src/routes/`** + **`src/controllers/`** — Health check endpoints
- **`src/web_server.py`** — FastAPI init + CORS + MCP SSE mount
- **`src/mcp_server.py`** — FastMCP instance creation
- **`src/main.py`** — Entry point (factory function for uvicorn)

### Transport modes
- `SERVER_MODE=stdio` — Local MCP with Claude (stdin/stdout)
- `SERVER_MODE=single-worker` — Dev HTTP with reload
- `SERVER_MODE=multi-worker` — Production (1 worker for SSE)

## Commands
```bash
pdm install              # Install deps
pdm run dev              # Dev server (reload)
pdm run test             # Run tests with coverage
pdm run lint             # Ruff linter
pdm run export           # Export requirements.txt
```

## Key patterns
- All tools use `with client:` context manager for auth
- `BaseCRUDService` handles generic list/get/create/update/delete
- JSON validation centralized in `src/utils/validators.py`
- Health checks at `/devops-awx-mcp/healthy` and `/devops-awx-mcp/liveness`

## Docker
- `Dockerfile.single_worker` — Dev
- `Dockerfile.multi_worker` — Production (compatible with AWX Jinja2 template)
