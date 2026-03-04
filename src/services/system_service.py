from src.client.ansible_client import AnsibleClient


class SystemService:
    def __init__(self, client: AnsibleClient):
        self.client = client

    def get_version(self) -> dict:
        return self.client.request("GET", "/api/v2/ping/")

    def get_dashboard(self) -> dict:
        return self.client.request("GET", "/api/v2/dashboard/")

    def get_metrics(self) -> dict:
        try:
            return self.client.request("GET", "/api/v2/metrics/")
        except Exception:
            url = f"{self.client.base_url}/api/v2/metrics/"
            response = self.client.raw_get(url)
            if response.status_code < 400:
                return {"status": "success", "raw_data": response.text[:1000]}
            raise
