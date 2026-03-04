import json

from src.services.base_service import BaseCRUDService
from src.services.job_service import JobService
from src.utils.validators import validate_json


def register_job_template_tools(mcp, service: BaseCRUDService, job_service: JobService):
    @mcp.tool()
    def list_job_templates(limit: int = 100, offset: int = 0) -> str:
        """List all job templates."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_job_template(template_id: int) -> str:
        """Get details about a specific job template."""
        with service.client:
            return json.dumps(service.get(template_id), indent=2)

    @mcp.tool()
    def create_job_template(
        name: str,
        inventory_id: int,
        project_id: int,
        playbook: str,
        credential_id: int = None,
        description: str = "",
        extra_vars: str = "{}",
    ) -> str:
        """Create a new job template."""
        try:
            validate_json(extra_vars, "extra_vars")
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {
                "name": name,
                "inventory": inventory_id,
                "project": project_id,
                "playbook": playbook,
                "description": description,
                "extra_vars": extra_vars,
                "job_type": "run",
                "verbosity": 0,
            }
            if credential_id:
                data["credential"] = credential_id
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_job_template(
        template_id: int,
        name: str = None,
        inventory_id: int = None,
        playbook: str = None,
        description: str = None,
        extra_vars: str = None,
    ) -> str:
        """Update an existing job template."""
        if extra_vars:
            try:
                validate_json(extra_vars, "extra_vars")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if inventory_id:
                data["inventory"] = inventory_id
            if playbook:
                data["playbook"] = playbook
            if description:
                data["description"] = description
            if extra_vars:
                data["extra_vars"] = extra_vars
            return json.dumps(service.update(template_id, data), indent=2)

    @mcp.tool()
    def delete_job_template(template_id: int) -> str:
        """Delete a job template."""
        with service.client:
            return json.dumps(service.delete(template_id), indent=2)

    @mcp.tool()
    def launch_job(template_id: int, extra_vars: str = None) -> str:
        """Launch a job from a job template."""
        if extra_vars:
            try:
                validate_json(extra_vars, "extra_vars")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            return json.dumps(job_service.launch_job(template_id, extra_vars), indent=2)
