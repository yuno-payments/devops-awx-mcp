import json

from src.client.ansible_client import AnsibleClient
from src.client.pagination import handle_pagination
from src.services.base_service import BaseCRUDService


def register_team_tools(mcp, service: BaseCRUDService, client: AnsibleClient):
    @mcp.tool()
    def list_teams(organization_id: int = None, limit: int = 100, offset: int = 0) -> str:
        """List teams, optionally filtered by organization."""
        with client:
            params = {"limit": limit, "offset": offset}
            endpoint = f"/api/v2/organizations/{organization_id}/teams/" if organization_id else "/api/v2/teams/"
            return json.dumps(handle_pagination(client, endpoint, params), indent=2)

    @mcp.tool()
    def get_team(team_id: int) -> str:
        """Get details about a specific team."""
        with client:
            return json.dumps(service.get(team_id), indent=2)

    @mcp.tool()
    def create_team(name: str, organization_id: int, description: str = "") -> str:
        """Create a new team."""
        with client:
            data = {"name": name, "organization": organization_id, "description": description}
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_team(team_id: int, name: str = None, description: str = None) -> str:
        """Update an existing team."""
        with client:
            data = {}
            if name:
                data["name"] = name
            if description:
                data["description"] = description
            return json.dumps(service.update(team_id, data), indent=2)

    @mcp.tool()
    def delete_team(team_id: int) -> str:
        """Delete a team."""
        with client:
            return json.dumps(service.delete(team_id), indent=2)
