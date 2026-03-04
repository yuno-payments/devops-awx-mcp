import json

from client.pagination import handle_pagination
from services.base_service import BaseCRUDService
from services.group_service import GroupService
from utils.validators import validate_json


def register_group_tools(mcp, service: BaseCRUDService, group_ops: GroupService):
    @mcp.tool()
    def list_groups(inventory_id: int, limit: int = 100, offset: int = 0) -> str:
        """List groups in an inventory."""
        with service.client:
            params = {"limit": limit, "offset": offset}
            return json.dumps(handle_pagination(service.client, f"/api/v2/inventories/{inventory_id}/groups/", params), indent=2)

    @mcp.tool()
    def get_group(group_id: int) -> str:
        """Get details about a specific group."""
        with service.client:
            return json.dumps(service.get(group_id), indent=2)

    @mcp.tool()
    def create_group(name: str, inventory_id: int, variables: str = "{}", description: str = "") -> str:
        """Create a new group in an inventory."""
        try:
            validate_json(variables, "variables")
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {"name": name, "inventory": inventory_id, "variables": variables, "description": description}
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_group(group_id: int, name: str = None, variables: str = None, description: str = None) -> str:
        """Update an existing group."""
        if variables:
            try:
                validate_json(variables, "variables")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if variables:
                data["variables"] = variables
            if description:
                data["description"] = description
            return json.dumps(service.update(group_id, data), indent=2)

    @mcp.tool()
    def delete_group(group_id: int) -> str:
        """Delete a group."""
        with service.client:
            return json.dumps(service.delete(group_id), indent=2)

    @mcp.tool()
    def add_host_to_group(group_id: int, host_id: int) -> str:
        """Add a host to a group."""
        with service.client:
            return json.dumps(group_ops.add_host(group_id, host_id), indent=2)

    @mcp.tool()
    def remove_host_from_group(group_id: int, host_id: int) -> str:
        """Remove a host from a group."""
        with service.client:
            return json.dumps(group_ops.remove_host(group_id, host_id), indent=2)
