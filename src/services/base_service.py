from client.ansible_client import AnsibleClient
from client.pagination import handle_pagination


class BaseCRUDService:
    def __init__(self, client: AnsibleClient, endpoint: str):
        self.client = client
        self.endpoint = endpoint

    def list(self, limit: int = 100, offset: int = 0, **filters) -> list[dict]:
        params = {"limit": limit, "offset": offset, **filters}
        return handle_pagination(self.client, self.endpoint, params)

    def get(self, resource_id: int) -> dict:
        return self.client.request("GET", f"{self.endpoint}{resource_id}/")

    def create(self, data: dict) -> dict:
        return self.client.request("POST", self.endpoint, data=data)

    def update(self, resource_id: int, data: dict) -> dict:
        return self.client.request("PATCH", f"{self.endpoint}{resource_id}/", data=data)

    def delete(self, resource_id: int) -> dict:
        self.client.request("DELETE", f"{self.endpoint}{resource_id}/")
        return {"status": "success", "message": f"Resource {resource_id} deleted"}
