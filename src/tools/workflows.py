import json

from src.services.base_service import BaseCRUDService
from src.services.workflow_service import WorkflowService
from src.utils.validators import validate_json


def register_workflow_tools(mcp, service: BaseCRUDService, workflow_ops: WorkflowService):
    @mcp.tool()
    def list_workflow_templates(limit: int = 100, offset: int = 0) -> str:
        """List all workflow templates."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_workflow_template(template_id: int) -> str:
        """Get details about a specific workflow template."""
        with service.client:
            return json.dumps(service.get(template_id), indent=2)

    @mcp.tool()
    def launch_workflow(template_id: int, extra_vars: str = None) -> str:
        """Launch a workflow from a workflow template."""
        if extra_vars:
            try:
                validate_json(extra_vars, "extra_vars")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            return json.dumps(workflow_ops.launch(template_id, extra_vars), indent=2)

    @mcp.tool()
    def list_workflow_jobs(status: str = None, limit: int = 100, offset: int = 0) -> str:
        """List all workflow jobs, optionally filtered by status."""
        with service.client:
            return json.dumps(workflow_ops.list_jobs(status=status, limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_workflow_job(job_id: int) -> str:
        """Get details about a specific workflow job."""
        with service.client:
            return json.dumps(workflow_ops.get_job(job_id), indent=2)

    @mcp.tool()
    def cancel_workflow_job(job_id: int) -> str:
        """Cancel a running workflow job."""
        with service.client:
            return json.dumps(workflow_ops.cancel_job(job_id), indent=2)
