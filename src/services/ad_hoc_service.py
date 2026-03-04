from src.client.ansible_client import AnsibleClient


class AdHocService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def run(self, inventory_id: int, credential_id: int, module_name: str, module_args: str,
            limit: str = "", verbosity: int = 0) -> dict:
        data = {
            "inventory": inventory_id,
            "credential": credential_id,
            "module_name": module_name,
            "module_args": module_args,
            "verbosity": verbosity,
        }
        if limit:
            data["limit"] = limit
        return self.client.request("POST", "/api/v2/ad_hoc_commands/", data=data)

    def get(self, command_id: int) -> dict:
        return self.client.request("GET", f"/api/v2/ad_hoc_commands/{command_id}/")

    def cancel(self, command_id: int) -> dict:
        try:
            return self.client.request("POST", f"/api/v2/ad_hoc_commands/{command_id}/cancel/")
        except Exception:
            response = self.client.request("GET", f"/api/v2/ad_hoc_commands/{command_id}/")
            status = response.get("status")
            if status in ("pending", "waiting", "running"):
                self.client.request("DELETE", f"/api/v2/ad_hoc_commands/{command_id}/")
                return {"status": "success", "message": f"Ad hoc command {command_id} cancelled via DELETE"}
            raise ValueError(f"Cannot cancel command in status: {status}")
