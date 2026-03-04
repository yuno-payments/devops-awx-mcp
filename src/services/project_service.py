from src.client.ansible_client import AnsibleClient


class ProjectService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def sync(self, project_id: int) -> dict:
        return self.client.request("POST", f"/api/v2/projects/{project_id}/update/")
