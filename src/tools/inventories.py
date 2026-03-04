import json

from services.base_service import BaseCRUDService


def register_inventory_tools(mcp, service: BaseCRUDService):
    @mcp.tool()
    def list_inventories(limit: int = 100, offset: int = 0) -> str:
        """List all inventories."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_inventory(inventory_id: int) -> str:
        """Get details about a specific inventory."""
        with service.client:
            return json.dumps(service.get(inventory_id), indent=2)

    @mcp.tool()
    def create_inventory(name: str, organization_id: int, description: str = "") -> str:
        """Create a new inventory."""
        with service.client:
            data = {"name": name, "description": description, "organization": organization_id}
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_inventory(inventory_id: int, name: str = None, description: str = None) -> str:
        """Update an existing inventory."""
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if description:
                data["description"] = description
            return json.dumps(service.update(inventory_id, data), indent=2)

    @mcp.tool()
    def delete_inventory(inventory_id: int) -> str:
        """Delete an inventory."""
        with service.client:
            return json.dumps(service.delete(inventory_id), indent=2)
