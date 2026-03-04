import json

from src.services.base_service import BaseCRUDService
from src.services.project_service import ProjectService
from src.utils.validators import validate_scm_type


def register_project_tools(mcp, service: BaseCRUDService, project_ops: ProjectService):
    @mcp.tool()
    def list_projects(limit: int = 100, offset: int = 0) -> str:
        """List all projects."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_project(project_id: int) -> str:
        """Get details about a specific project."""
        with service.client:
            return json.dumps(service.get(project_id), indent=2)

    @mcp.tool()
    def create_project(
        name: str,
        organization_id: int,
        scm_type: str,
        scm_url: str = None,
        scm_branch: str = None,
        credential_id: int = None,
        description: str = "",
    ) -> str:
        """Create a new project."""
        try:
            validate_scm_type(scm_type)
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})

        if scm_type != "manual" and not scm_url:
            return json.dumps({"status": "error", "message": "SCM URL is required for non-manual SCM types"})

        with service.client:
            data = {"name": name, "organization": organization_id, "scm_type": scm_type, "description": description}
            if scm_url:
                data["scm_url"] = scm_url
            if scm_branch:
                data["scm_branch"] = scm_branch
            if credential_id:
                data["credential"] = credential_id
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_project(
        project_id: int,
        name: str = None,
        scm_type: str = None,
        scm_url: str = None,
        scm_branch: str = None,
        description: str = None,
    ) -> str:
        """Update an existing project."""
        if scm_type:
            try:
                validate_scm_type(scm_type)
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})

        with service.client:
            data = {}
            if name:
                data["name"] = name
            if scm_type:
                data["scm_type"] = scm_type
            if scm_url:
                data["scm_url"] = scm_url
            if scm_branch:
                data["scm_branch"] = scm_branch
            if description:
                data["description"] = description
            return json.dumps(service.update(project_id, data), indent=2)

    @mcp.tool()
    def delete_project(project_id: int) -> str:
        """Delete a project."""
        with service.client:
            return json.dumps(service.delete(project_id), indent=2)

    @mcp.tool()
    def sync_project(project_id: int) -> str:
        """Sync a project with its SCM source."""
        with service.client:
            return json.dumps(project_ops.sync(project_id), indent=2)
