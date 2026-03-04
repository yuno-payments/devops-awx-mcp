
from src.client.ansible_client import AnsibleClient
from src.client.pagination import handle_pagination


class JobService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def list_jobs(self, status: str = None, limit: int = 100, offset: int = 0) -> list[dict]:
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return handle_pagination(self.client, "/api/v2/jobs/", params)

    def get_job(self, job_id: int) -> dict:
        return self.client.request("GET", f"/api/v2/jobs/{job_id}/")

    def cancel_job(self, job_id: int) -> dict:
        return self.client.request("POST", f"/api/v2/jobs/{job_id}/cancel/")

    def get_events(self, job_id: int, limit: int = 100, offset: int = 0) -> list[dict]:
        params = {"limit": limit, "offset": offset}
        return handle_pagination(self.client, f"/api/v2/jobs/{job_id}/job_events/", params)

    def get_stdout(self, job_id: int, fmt: str = "txt") -> dict:
        if fmt not in ("txt", "html", "json", "ansi"):
            raise ValueError("Invalid format. Must be one of: txt, html, json, ansi")

        if fmt != "json":
            url = f"{self.client.base_url}/api/v2/jobs/{job_id}/stdout/?format={fmt}"
            response = self.client.raw_get(url)
            return {"status": "success", "stdout": response.text}
        else:
            return self.client.request("GET", f"/api/v2/jobs/{job_id}/stdout/?format={fmt}")

    def launch_job(self, template_id: int, extra_vars: str = None) -> dict:
        data = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.client.request("POST", f"/api/v2/job_templates/{template_id}/launch/", data=data)
