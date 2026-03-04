import json

from services.job_service import JobService


def register_job_tools(mcp, job_service: JobService):
    @mcp.tool()
    def list_jobs(status: str = None, limit: int = 100, offset: int = 0) -> str:
        """List all jobs, optionally filtered by status."""
        with job_service.client:
            return json.dumps(job_service.list_jobs(status=status, limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_job(job_id: int) -> str:
        """Get details about a specific job."""
        with job_service.client:
            return json.dumps(job_service.get_job(job_id), indent=2)

    @mcp.tool()
    def cancel_job(job_id: int) -> str:
        """Cancel a running job."""
        with job_service.client:
            return json.dumps(job_service.cancel_job(job_id), indent=2)

    @mcp.tool()
    def get_job_events(job_id: int, limit: int = 100, offset: int = 0) -> str:
        """Get events for a specific job."""
        with job_service.client:
            return json.dumps(job_service.get_events(job_id, limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_job_stdout(job_id: int, format: str = "txt") -> str:
        """Get the standard output of a job."""
        with job_service.client:
            try:
                return json.dumps(job_service.get_stdout(job_id, fmt=format), indent=2)
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
