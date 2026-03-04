import json

from client.ansible_client import AnsibleClient
from client.pagination import handle_pagination
from services.base_service import BaseCRUDService
from utils.validators import validate_json


def register_host_tools(mcp, service: BaseCRUDService, client: AnsibleClient):
    @mcp.tool()
    def list_hosts(inventory_id: int = None, limit: int = 100, offset: int = 0) -> str:
        """List hosts, optionally filtered by inventory."""
        with client:
            params = {"limit": limit, "offset": offset}
            endpoint = f"/api/v2/inventories/{inventory_id}/hosts/" if inventory_id else "/api/v2/hosts/"
            return json.dumps(handle_pagination(client, endpoint, params), indent=2)

    @mcp.tool()
    def get_host(host_id: int) -> str:
        """Get details about a specific host."""
        with client:
            return json.dumps(service.get(host_id), indent=2)

    @mcp.tool()
    def create_host(name: str, inventory_id: int, variables: str = "{}", description: str = "") -> str:
        """Create a new host in an inventory."""
        try:
            validate_json(variables, "variables")
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with client:
            data = {"name": name, "inventory": inventory_id, "variables": variables, "description": description}
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_host(host_id: int, name: str = None, variables: str = None, description: str = None) -> str:
        """Update an existing host."""
        if variables:
            try:
                validate_json(variables, "variables")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with client:
            data = {}
            if name:
                data["name"] = name
            if variables:
                data["variables"] = variables
            if description:
                data["description"] = description
            return json.dumps(service.update(host_id, data), indent=2)

    @mcp.tool()
    def delete_host(host_id: int) -> str:
        """Delete a host."""
        with client:
            return json.dumps(service.delete(host_id), indent=2)
