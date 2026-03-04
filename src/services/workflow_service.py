from src.client.ansible_client import AnsibleClient
from src.client.pagination import handle_pagination


class WorkflowService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def launch(self, template_id: int, extra_vars: str = None) -> dict:
        data = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.client.request("POST", f"/api/v2/workflow_job_templates/{template_id}/launch/", data=data)

    def list_jobs(self, status: str = None, limit: int = 100, offset: int = 0) -> list[dict]:
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return handle_pagination(self.client, "/api/v2/workflow_jobs/", params)

    def get_job(self, job_id: int) -> dict:
        return self.client.request("GET", f"/api/v2/workflow_jobs/{job_id}/")

    def cancel_job(self, job_id: int) -> dict:
        return self.client.request("POST", f"/api/v2/workflow_jobs/{job_id}/cancel/")
