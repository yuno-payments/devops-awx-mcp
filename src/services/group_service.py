from client.ansible_client import AnsibleClient


class GroupService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def add_host(self, group_id: int, host_id: int) -> dict:
        return self.client.request("POST", f"/api/v2/groups/{group_id}/hosts/", data={"id": host_id})

    def remove_host(self, group_id: int, host_id: int) -> dict:
        self.client.request("POST", f"/api/v2/groups/{group_id}/hosts/", data={"id": host_id, "disassociate": True})
        return {"status": "success", "message": f"Host {host_id} removed from group {group_id}"}
