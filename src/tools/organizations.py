import json

from src.services.base_service import BaseCRUDService


def register_organization_tools(mcp, service: BaseCRUDService):
    @mcp.tool()
    def list_organizations(limit: int = 100, offset: int = 0) -> str:
        """List all organizations."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_organization(organization_id: int) -> str:
        """Get details about a specific organization."""
        with service.client:
            return json.dumps(service.get(organization_id), indent=2)

    @mcp.tool()
    def create_organization(name: str, description: str = "") -> str:
        """Create a new organization."""
        with service.client:
            data = {"name": name, "description": description}
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_organization(organization_id: int, name: str = None, description: str = None) -> str:
        """Update an existing organization."""
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if description:
                data["description"] = description
            return json.dumps(service.update(organization_id, data), indent=2)

    @mcp.tool()
    def delete_organization(organization_id: int) -> str:
        """Delete an organization."""
        with service.client:
            return json.dumps(service.delete(organization_id), indent=2)
