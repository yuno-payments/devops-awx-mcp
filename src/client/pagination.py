from src.client.ansible_client import AnsibleClient


def handle_pagination(client: AnsibleClient, endpoint: str, params: dict = None) -> list[dict]:
    if params is None:
        params = {}

    results = []
    next_url = endpoint

    while next_url:
        response = client.request("GET", next_url, params=params)
        if "results" in response:
            results.extend(response["results"])
        else:
            return [response]

        next_url = response.get("next")
        if next_url:
            params = None

    return results
